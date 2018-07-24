from order.models import CbgOrders, CbgRechargeRecord, CbgCurrencyConsumeRecord, CbgOrderDetail, CbgOrderReductionLog
from user.models import UserProfile
from coupon.models import CbgCouponUserRelation
from order.functions import paysapi_signature, check_paysapi_notify_signature, prepare_order_pay, start_task, \
                            order_bill, check_reduction_log
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from unit.decoration import ajax_refresh, sms_send
from unit.utility import *


def currency_recharge_page(request, response, render):
    """充值货币的页面"""
    return render_to_response(request, response, render, 'order/currency_recharge.html')


@transaction.atomic
def build_curency_order_api(request, response, render, currency, istype):
    """生成充值货币订单的api"""
    notify_url = '%s/order/currency_paysapi_notify' % settings.RUN_URL
    return_url = '%s/order/currency_pay_success' % settings.RUN_URL
    goodsname = '货币充值'
    give = 0
    if currency == '100':
        give = 5
    elif currency == '200':
        give = 12
    elif currency == '300':
        give = 21
    elif currency == '500':
        give = 45
    # 创建充值记录
    profile = UserProfile.objects.select_for_update().get(user_id=request.user.id)
    record, is_new = CbgRechargeRecord.objects.get_or_create(
        user_id=request.user.id,
        status='待付款',
        defaults={
            'quantity': int(currency) * 100,
            'give': give * 100,
            'create_time': render['timenow'],
            'left_quantity': profile.currency
        })
    if not is_new:
        record.quantity = int(currency) * 100
        record.give = give * 100
        record.create_time = render['timenow']
        record.left_quantity = profile.currency
        record.save()

    # 加密订单
    prpcrypt_orderid = Prpcrypt.encrypt('currency_%s' % record.id)  # 这里需要加prefix与订单相区别
    prpcrypt_orderuid = Prpcrypt.encrypt(record.user_id)
    # 生成token
    pay_token = paysapi_signature('%.2f' % (int(record.quantity) / 100), istype, prpcrypt_orderid,
                                    prpcrypt_orderuid, goodsname, notify_url, return_url)
    return response_json('SUCC', description='生成充值记录成功', msg='BuilSucc', token=pay_token)


@transaction.atomic
def currency_pay_success(request, response, render):
    """货币支付成功的跳转页面"""
    record_id = request.GET.get('orderid', '')
    try:
        record_id = Prpcrypt.decrypt(record_id).split('currency_')[1]
        CbgRechargeRecord.objects.get(id=record_id)
    except CbgRechargeRecord.DoesNotExist:
        return HttpResponseForbidden("can't find this record")
    except:
        return HttpResponseForbidden("can't decrypt")
    return render_to_response(request, response, render, 'order/currency_pay_success.html')


@transaction.atomic
@csrf_exempt
def currency_paysapi_notify(request, response, render):
    """货币支付成功的回调接口"""
    istype = request.GET.get('istype')
    need_param_dict = {'paysapi_id': '', 'orderid': '', 'price': '', 'realprice': '', 'orderuid': '', 'key': ''}
    for key in need_param_dict.keys():
        need_param_dict[key] = request.POST.get(key)
        if not need_param_dict[key]:
            return HttpResponseForbidden('"%s" need' % key)
    if not check_paysapi_notify_signature(need_param_dict):
        return HttpResponseForbidden('error key')
    record_id = need_param_dict['orderid']
    user_id = need_param_dict['orderuid']
    try:
        # 货币第三方支付需要加前缀  currency_2 来和order_id=2的做区别
        record_id = Prpcrypt.decrypt(record_id).split('currency_')[1]
        user_id = Prpcrypt.decrypt(user_id)
        record = CbgRechargeRecord.objects.get(id=record_id)
    except CbgOrders.DoesNotExist:
        # 有支付回调但是可能找不到对应的订单
        settings.log_paysapi.info('id: {0} user_id: {1} price: {1} real_price'.format(
            record_id, user_id, need_param_dict['price'], need_param_dict['realprice']
        ))
        return HttpResponseForbidden("can't find this order")
    #编码的错误
    except:
        return HttpResponseForbidden("can't decrypt")
    profile = UserProfile.objects.select_for_update().get(user_id=user_id)
    profile.currency += int(record.quantity) + int(record.give)
    profile.give_currency += int(record.give)
    profile.save()
    record.status = '已支付'
    record.pay_time = render['timenow']
    record.pay_tradeno = need_param_dict['paysapi_id']
    record.pay_channel = istype
    record.left_quantity = profile.currency
    record.save()
    return HttpResponse('ok')


def currency_log_page(request, response, render):
    """货币使用记录"""
    return render_to_response(request, response, render, 'order/currency_log.html')


@ajax_refresh(order_limit=('-id',))
def currency_recharge_log_api(request, response, render):
    """货币充值记录"""
    offset, order_by, int_limit, filter_ = render['query_params']
    filter_['status'] = '已支付'
    filter_['user_id'] = request.user.id
    queryset = CbgRechargeRecord.json_queryset(order_by=order_by, offset=offset, limit=int_limit, filter_=filter_)
    return {'query_list': queryset}


@ajax_refresh(order_limit=('-id',))
def currency_consume_log_api(request, response, render):
    """货币使用记录"""
    offset, order_by, int_limit, filter_ = render['query_params']
    filter_['user_id'] = request.user.id
    queryset = CbgCurrencyConsumeRecord.json_queryset(order_by=order_by, offset=offset, limit=int_limit, filter_=filter_)
    return {'query_list': queryset}


@transaction.atomic
@sms_send
def currency_pay_page(request, response, render, order_id):
    """盒币支付页面"""
    coupon_id = request.GET.get('coupon_id')
    b, result = prepare_order_pay(request, order_id, coupon_id)
    if b is False:
        return render_to_error_response(request, response, render, result)
    order, my_coupon= result
    if order.pay_status != '待付款':
        return render_to_error_response(request, response, render, '该订单不处于待付款状态')
    profile = UserProfile.objects.get(user_id=request.user.id)
    if profile.currency < order.real_price:
        return render_to_error_response(request, response, render, '盒币余额不够！')
    render['order'] = order
    render['my_coupon'] = my_coupon
    render['reduction'] = order.price - order.real_price
    return render_to_response(request, response, render, 'order/templates/currency_pay.html')


@transaction.atomic
def currency_pay_api(request, response, render, captcha, order_id):
    """盒币支付api"""
    # 1. 校验验证码
    now = render['timenow']
    if captcha.encode() != settings.redis3.get('currency_pay_captcha_%s' % request.user.username):
        return response_json(retcode='FAIL', msg='CatpchaError', description='验证码错误')
    # 2.校验订单
    try:
        order = CbgOrders.objects.get(id=order_id, is_delete=0)
    except:
        return response_json(retcode='FAIL', msg='ErrorOrder', description='订单号错误')
    if order.status != '待付款':
        return response_json(retcode='FAIL', msg='ErrorStatus', description='状态非待付款')
    # 校验金额
    profile = UserProfile.objects.select_for_update().get(user_id=request.user.id)
    if order.real_price > profile.currency:
        return response_json(retcode='FAIL', msg='MissCurrency', description='金额不够本次支付')
    # 校验优惠是否过期
    disable_reduction, _ = check_reduction_log(order)
    if disable_reduction:
        error_msg = "您的【%s】已经过期，请重新支付" % disable_reduction[0].alias
        return render_to_error_response(request, response, render, error_msg)

    profile.currency -= order.real_price
    profile.save()
    # 更新订单   # todo 是否校验优惠券的可用？ 不要 因为在选择优惠券的时候用户已经被限制住了
    order_detail = CbgOrderDetail.objects.get(order_id=order.id)
    order_bill(order, order_detail, 4, order.id)
    CbgCurrencyConsumeRecord.objects.create(user_id=request.user.id, quantity=order.real_price, left_quantity=profile.currency,
                                         order_id=order.id, brief=order.service_name + '(%s天)' % order_detail.service_time)
    start_task(order, order_detail)
    settings.redis3.delete("currency_pay_captcha_%s" % request.user.username)
    return response_json('SUCC', description='付款成功', msg='PaySucc', encrpt_orderid=Prpcrypt.encrypt(str(order.id)))







