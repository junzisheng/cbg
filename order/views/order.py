from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

from order.models import CbgOrders, CbgOrderDetail, CbgOrderReductionLog
from coupon.models import CbgCouponUserRelation
from order.functions import paysapi_signature, check_paysapi_notify_signature, prepare_order_pay, start_task, \
                            check_reduction_log, order_bill
from coupon.functions import get_user_service_coupon
from unit.decoration import ajax_refresh
from unit.utility import *


# todo 降价推送警告用户至少选择一种推送方式
@transaction.atomic
def pay_page(request, response, render, order_id):
    """
    订单页面
    """
    try:
        order = CbgOrders.objects.select_for_update().get(id=order_id, user_id=request.user.id, is_delete=0)
    except CbgOrders.DoesNotExist:
        return render_to_error_response(request, response, render, error_msg='错误的参数！')
    if order.status not in ('初始状态', '待付款'):
        return render_to_error_response(request, response, render, error_msg='错误的请求！')
    # todo 1.判断这个服务有没有优惠活动
    render['order'] = order
    render['currency'] = '%.2f' % (request.user.userprofile.currency / 100)
    # 获取用户可以使用的优惠券信息
    if order.status == '初始状态':
        render['coupon_list'] = json.dumps(get_user_service_coupon(request, order.service_id, order))
    # 获取之前用户选择的优惠信息
    else:
        render['disable_reduction'], render['awalid_reduction'] = check_reduction_log(order)

    return render_to_response(request, response, render, 'order/templates/pay_page.html')


@transaction.atomic
def get_pay_token_api(request, response, render,  pay_type):
    """获取支付的token"""
    notify_url = '%s/order/order_paysapi_notify' % settings.RUN_URL
    return_url = '%s/order/order_pay_success' % settings.RUN_URL
    order_id = request.GET.get('order_id')
    # url_params = ""
    coupon_id = request.GET.get('coupon_id')
    b, result = prepare_order_pay(request, order_id, coupon_id)
    if b is False:
        return response_json(retcode='FAIL', description=result)
    order, my_coupon = result
    # if my_coupon is not None:  # 把使用的优惠券信息放到回掉的url中
    #     url_params = "&coupon_rel_id=" % my_coupon.id
    # 1. 计算价格
    prpcrypt_orderid = Prpcrypt.encrypt(order.id)
    prpcrypt_orderuid = Prpcrypt.encrypt(order.user_id)
    pay_token =  paysapi_signature('%.2f' % (order.real_price / 100), pay_type, prpcrypt_orderid,
                                     prpcrypt_orderuid, order.service_name, notify_url, return_url)
    return response_json(retcode='SUCC', msg='GetTokenSucc', token=pay_token)



@transaction.atomic
@csrf_exempt
def order_paysapi_notify(request, response, render):
    """
    第三方支付成功后的回调接口
    POST
    :param paysapi_id:  paysapi中的唯一id
    :param orderid:  加密的orderid
    :param price:    传入的订单价格
    :param realprice: 实际支付的价格  paysapi根据同时支付的人数价格会有0.01-0.02的波动
    :param: orderuid: 传入的orderuid 加密
    :key: 需要校验key
    """
    # 校验参数
    istype = request.GET.get('istype')
    need_param_dict = {'paysapi_id': '', 'orderid': '', 'price': '', 'realprice': '', 'orderuid': '', 'key': ''}
    for key in need_param_dict.keys():
        need_param_dict[key] = request.POST.get(key)
        if not need_param_dict[key]:
            return HttpResponseForbidden('"%s" need' % key)
    if not check_paysapi_notify_signature(need_param_dict):
        return HttpResponseForbidden('error key')
    order_id = need_param_dict['orderid']
    user_id = need_param_dict['orderuid']
    try:
        order_id = Prpcrypt.decrypt(order_id)
        user_id = Prpcrypt.decrypt(user_id)
        order = CbgOrders.objects.select_for_update().get(id=order_id, is_delete=0)
    except CbgOrders.DoesNotExist:
        # 有支付回调但是可能找不到对应的订单
        settings.log_paysapi.info('id: {0} user_id: {1} price: {1} real_price'.format(
            order_id, user_id, need_param_dict['price'], need_param_dict['realprice']
        ))
        return HttpResponseForbidden("can't find this order")
    #编码的错误
    except:
        return HttpResponseForbidden("can't decrypt")
    # 更新订单信息
    order_detail = CbgOrderDetail.objects.get(order_id=order.id)
    order_bill(order, order_detail, istype, need_param_dict['payapi_id'])
    # 开启爬取的任务
    start_task(order, order_detail)
    return HttpResponse('ok')


def order_pay_success(request, response, render):
    orderid = request.GET.get('orderid', '')
    try:
        orderid = Prpcrypt.decrypt(orderid)
        order = CbgOrders.objects.get(id=orderid, is_delete=0)
    except CbgOrders.DoesNotExist:
        return HttpResponseForbidden("can't find this order")
    except:
        return HttpResponseForbidden("can't decrypt")
    if order.pay_status != '已支付':
        return render_to_error_response(request, response, render, '订单状态尚未更新，请刷新页面')
    render['order'] = order
    # 获取优惠记录
    _, render['awalid_reduction'] = check_reduction_log(order)
    return render_to_response(request, response, render, 'order/templates/pay_success.html')


def order_main(request, response, render):
    render['status'] = request.GET.get('status', '待付款')
    if render['status'] not in ('待付款', '进行中', '已完成', '全部订单'):
        return render_to_error_response(request, response, render, '错误的请求')
    return render_to_response(request, response, render, 'order/templates/main.html')


def order_detail(request, response, render, order_id):
    try:
        order = CbgOrders.objects.get(id=order_id, user_id=request.user.id, is_delete=0)
    except:
        return render_to_error_response(request, response, render, '该订单不存在！')
    filter_ = {'order_id': order}
    if order.status == '待付款':
        filter_['deadline__gte'] = render['timenow']
    render['disable_reduction'], render['awalid_reduction'] = check_reduction_log(order)
    render['order'] = order
    return render_to_response(request, response, render, 'order/templates/order_detail.html')


@ajax_refresh(order_limit=('-id'), filter_limit={'status': '已支付|待付款|进行中|已完成|all'})
def pull_order_data(request, response, render):
    """获取订单数据"""
    offset, order_by, int_limit, filter_ = render['query_params']
    filter_['user_id'] = request.user.id
    filter_['is_delete'] = 0
    query_list = CbgOrders.json_queryset(order_by=order_by, offset=offset, limit=int_limit, filter_=filter_, exclude={'status': '初始状态'})
    for _query in query_list:
        _info = _query['service_info'].split('|', 4)  # 推送方式|服务时长|是否第一轮推送|是否降价推送|memo
        _query['push_type'] = _info[0]
        _query['service_time'] = _info[1]
        _query['first_round_push'] = _info[2] == 'True'
        _query['price_down_push'] = _info[3] == 'True'
        _query['memo'] = _info[4]
    return {'query_list': query_list}


@transaction.atomic
def delete_order(request, response, render, order_id):
    """删除订单"""
    try:
        order = CbgOrders.objects.get(user_id=request.user.id, id=order_id, is_delete=0)
        order.is_delete = 1
        order.save()
        # 删除记录的优惠记录
        CbgOrderReductionLog.objects.filter(order_id=order.id).delete()
        # 释放使用的优惠券
        CbgCouponUserRelation.objects.filter(order_id=order.id).update(status=0)
    except:
        return response_json(retcode='FAIL', msg="ErrorOid", description='错误的请求！')
    return response_json(retcode='SUCC', description='删除成功')
