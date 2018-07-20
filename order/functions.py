import datetime
import hashlib

from django.conf import settings
from order.models import CbgOrders, CbgOrderReductionLog, CbgOrderDetail
from coupon.models import CbgCouponUserRelation
from crawl_celery.tasks import crawl_task


def paysapi_signature(price, istype, orderid, orderuid, goodsname, notify_url, return_url, url_params=""):
    """生成条状payapi第三方支付网页所需的post参数"""
    param = {
        'goodsname': goodsname,
        'istype': istype,
        'notify_url': notify_url + '?istype=%s' % istype + url_params,
        'orderid': orderid,
        'orderuid': orderuid,
        'price': price,
        'return_url': return_url,
        'token': settings.PAYS_API['token'],
        'uid': settings.PAYS_API['uid'],
    }
    param_keys = list(param.keys())
    param_keys.sort()
    to_signature_str = ''
    for key in param_keys:
        to_signature_str += str(param[key]).lower()
    param['key'] = hashlib.md5(to_signature_str.encode()).hexdigest()
    return param


# def check_paysapi_notify_signature(payapi_id, orderid, price, realprice, orderuid, signature):
def check_paysapi_notify_signature(params):
    """payapi回调生成签名"""
    key = params.pop('key')
    params['token'] = settings.PAYS_API['token']
    param_keys = list(params.keys())
    param_keys.sort()
    to_signature_str = ''
    for k in param_keys:
        to_signature_str += str(params[k]).lower()
    signature = hashlib.md5(to_signature_str.encode()).hexdigest()
    return signature == key


def prepare_order_pay(request, order_id, coupon_id):
    """订单支付前的处理"""
    now = datetime.datetime.now()
    today = now.date()
    try:
        my_coupon = None
        order = CbgOrders.objects.select_for_update().get(id=order_id, user_id=request.user.id)
        if order.status not in ('待付款', '初始状态'):
            return False, '错误的订单号！'
        if order.status == '待付款':
            check_reduction_log(order,  revise=True)
            return True, (order, None)
        order.status = '待付款'
        order.real_price = order.price  # 价格以基本价格为准, 优惠可能随时在变
        if coupon_id:
            my_coupon = CbgCouponUserRelation.objects.select_for_update().get(id=coupon_id, user_id=request.user.id)
            coupon = my_coupon.coupon
            if my_coupon.status == 1:
                return False, '您选择的已被其它订单占用，请删除该订单释放优惠券！'
            if my_coupon.status == 2:
                return False, '您选择优惠券已被使用！'
            if my_coupon.expire_time < today:
                return False, '您选择的优惠券已过期！'
            if my_coupon.acquire_time > today:
                return False, '您选择的优惠券尚未到使用时间！'
            if coupon.fill > order.price:
                return False, '您选择的优惠券需要满%s元才能使用！' % coupon.fill / 100
            # 校验该优惠券的服务类型
            if str(order.service_id) not in my_coupon.service_ids.split(','):
                return False, '您选择的优惠券无法用于【%s】' % order.service_name
            # 计算优惠价格
            reduction = coupon.get_reduction(order.real_price)
            order.real_price = order.real_price - reduction if order.real_price > reduction else 0.01
            # 更新优惠券关系
            my_coupon.status = 1
            my_coupon.order_id = order.id
            my_coupon.save()
            # 记录优惠信息  一种优惠只能有一条记录
            CbgOrderReductionLog.objects.create(
                order_id=order.id,
                style=1,
                alias=coupon.coupon_name,
                user_id=request.user.id,
                coupon_rel_id=my_coupon.id,
                reduction=reduction,
                deadline=my_coupon.expire_time + datetime.timedelta(days=1),
                create_time=now,
                pay_success= False,
            )
        order.save()
        return True, (order, my_coupon)
    except Exception as e:
        return False, '错误的请求'


def check_reduction_log(order, revise=True):
    """校验优惠是否过期"""
    now = datetime.datetime.now()
    redu_list = CbgOrderReductionLog.objects.filter(order_id=order.id)  # 获取下单时所有的优惠信息
    if redu_list and redu_list[0].pay_sucess:  # 如果这个订单已经支付了
        return [], list(redu_list)
    disable_reduction = [_x for _x in redu_list if _x.deadline < now]
    awalid_reduction = [_x for _x in redu_list if _x.deadline >= now]
    # 如果有失效的优惠信息, 重新计算价格
    if disable_reduction and revise:
        # 删除无效的优惠记录
        CbgOrderReductionLog.objects.filter(id__in=[_x.id for _x in disable_reduction]).delete()
        # 先计算优惠券， 再计算活动
        coupon_redu = [_x for _x in awalid_reduction if _x.style == 1]
        order.real_price = order.price
        if coupon_redu:
            coupon_rel = coupon_redu[0].coupon_rel  # 一个订单只能使用一个优惠券
            coupon = coupon_rel.coupon
            order.real_price -= coupon.get_reduction(order.price)
            order.real_price = 0.01 if order.real_price <= 0 else order.real_price
        order.save()
    return disable_reduction, awalid_reduction


def start_task(order, order_detail):
    """开启订单任务"""
    now = datetime.datetime.now()
    service_deadline = now + datetime.timedelta(days=order_detail.service_time)
    crawl_task.delay(order.service_id, order_detail.crawl_url, {
        'order_id': order.id,
        'memo': order_detail.memo,
        'user_id': order.user_id,
        'push_type': order_detail.push_type,
        'end_time': datetime.datetime.strftime(service_deadline, '%Y-%m-%d %H:%M:%S'),
        'time_range': {'days': 1},
        'first_round_push': order_detail.first_round_push,
        'price_down_push': order_detail.price_down_push,
        'umobile': order.user.username
    })


def order_bill(order, order_detail, pay_channel, pay_tradeno):
    """订单结算"""
    now = datetime.datetime.now()
    order.pay_status = '已支付'
    order.status = '进行中'
    order.pay_channel = pay_channel
    order.pay_time = now
    order.pay_tradeno = pay_tradeno
    order.start_time = now
    order.save()
    # 记录服务的销售情况
    order.service.count_buy += order_detail.service_time
    order.service.count_price += order.real_price
    order.service.save()
    # 更新优惠信息
    CbgOrderReductionLog.objects.filter(order_id=order.id).update(pay_success=True)
    # 将使用的优惠券更新
    CbgCouponUserRelation.objects.select_for_update().filter(order_id=order.id). \
        update(status=2, usage_time=now)

