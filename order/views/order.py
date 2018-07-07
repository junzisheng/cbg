from order.models import CrawlOrders
from ..functions import paysapi_signature, check_paysapi_notify_signature
from django.http import HttpResponseForbidden
from crawl_celery.tasks import crawl_task
from django.views.decorators.csrf import csrf_exempt
from unit.decoration import ajax_refresh
from unit.utility import *


# todo 降价推送警告用户至少选择一种推送方式
def pay_page(request, response, render, order_id):
    """
    订单页面
    """
    notify_url = '%s/order/order_paysapi_notify' % settings.RUN_URL
    return_url = '%s/order/order_pay_success' % settings.RUN_URL
    goodsname = '召唤兽提醒服务'
    try:
        order = CrawlOrders.objects.get(id=order_id, user_id=request.user.id, is_delete=0)
    except CrawlOrders.DoesNotExist:
        return render_to_error_response(request, response, render, error_msg='错误的参数！')
    if order.status != '待付款':
        return render_to_error_response(request, response, render, error_msg='该订单不处于待付款状态！')
    # 获取加密的order_oid和orderuid
    prpcrypt_orderid = Prpcrypt.encrypt(order.id)
    prpcrypt_orderuid = Prpcrypt.encrypt(order.user_id)
    render['order'] = order
    render['ali_payapi_post_params'] = paysapi_signature('%.2f' % (order.real_price / 100), 1, prpcrypt_orderid,
                                                         prpcrypt_orderuid, goodsname, notify_url, return_url)
    render['wx_payapi_post_params'] = paysapi_signature('%.2f' % (order.real_price / 100), 2, prpcrypt_orderid,
                                                        prpcrypt_orderuid, goodsname, notify_url, return_url)
    render['currency'] = '%.2f' % (request.user.userprofile.currency / 100)
    return render_to_response(request, response, render, 'order/pay_page.html')


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
        order = CrawlOrders.objects.get(id=order_id, is_delete=0)
    except CrawlOrders.DoesNotExist:
        # 有支付回调但是可能找不到对应的订单
        settings.log_paysapi.info('id: {0} user_id: {1} price: {1} real_price'.format(
            order_id, user_id, need_param_dict['price'], need_param_dict['realprice']
        ))
        return HttpResponseForbidden("can't find this order")
    #编码的错误
    except:
        return HttpResponseForbidden("can't decrypt")
    now = render['timenow']
    order.pay_status = '已支付'
    order.status = '进行中'
    order.pay_channel = istype
    order.pay_time = now
    order.pay_tradeno = need_param_dict['paysapi_id']
    order.start_time = now
    order.save()
    service_deadline = now + datetime.timedelta(days=order.service_time)
    # 开启爬取的任务
    crawl_task.delay('bb', order.crawl_url, {
        'order_id': order.id,
        'memo': order.memo,
        'user_id': order.user_id,
        'push_type': order.push_type,
        'end_time': datetime.datetime.strftime(service_deadline, '%Y-%m-%d %H:%M:%S'),
        'time_range': {'days': 1},
        'first_round_push': order.first_round_push,
        'price_down_push': order.price_down_push,
        'umobile': order.umobile
    })
    return HttpResponse('ok')


def order_pay_success(request, response, render):
    orderid = request.GET.get('orderid', '')
    try:
        orderid = Prpcrypt.decrypt(orderid)
        order = CrawlOrders.objects.get(id=orderid, is_delete=0)
    except CrawlOrders.DoesNotExist:
        return HttpResponseForbidden("can't find this order")
    except:
        return HttpResponseForbidden("can't decrypt")
    if order.pay_status != '已支付':
        return render_to_error_response(request, response, render, '订单状态尚未更新，请刷新页面')
    render['order'] = order
    return render_to_response(request, response, render, 'order/pay_success.html')


def order_main(request, response, render):
    render['status'] = request.GET.get('status', '待付款')
    if render['status'] not in ('待付款', '进行中', '已完成', '全部订单'):
        return render_to_error_response(request, response, render, '错误的请求')
    return render_to_response(request, response, render, 'order/main.html')


def order_detail(request, response, render, order_id):
    try:
        render['order'] = CrawlOrders.objects.get(id=order_id, user_id=request.user.id)
    except:
        return render_to_error_response(request, response, render, '错误的订单号！')
    return render_to_response(request, response, render, 'order/order_detail.html')


@ajax_refresh(order_limit=('-id'), filter_limit={'status': '已支付|待付款|进行中|已完成|all'})
def pull_order_data(request, response, render):
    """获取订单数据"""
    offset, order_by, int_limit, filter_ = render['query_params']
    filter_['user_id'] = request.user.id
    filter_['is_delete'] = 0
    query_list = CrawlOrders.json_queryset(order_by=order_by, offset=offset, limit=int_limit, filter_=filter_)
    return {'query_list': query_list}


def delete_order(request, response, render, order_id):
    """删除订单"""
    CrawlOrders.objects.filter(user_id=request.user.id, id=order_id, is_delete=0).update(is_delete=1)
    if request.is_ajax():
        return response_json(retcode='SUCC', description='删除成功')
    else:
        return render_to_response(request, response, render, 'order/main.html')
