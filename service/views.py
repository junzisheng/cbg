# encoding=utf-8
from django.http import HttpResponseRedirect
from order.models import CrawlOrders
from unit.utility import *
from .functions import bb_params_handle, role_params_handel, equip_params_handel
from unit.decoration import banner
from unit.functions import normal_request


type_handle_func_dict = {
    'baobao': bb_params_handle,
    'equip': equip_params_handel,
    'role': role_params_handel,
}


@banner('促销')
def index(request, response, render):
    """服务列表页面"""
    return render_to_response(request, response, render, 'service/index.html')


def service_page(request, response, render, type):
    """服务detail， type: 召唤兽|装备|角色"""
    render['params'] = request.GET.get('params', '')
    return render_to_response(request, response, render, 'service/search_page.html')


def crawl_request(request, response, render):
    """
    获取【人物】爬取的url 这里还是要用ajax请求， 防止刷新重复提交表单
    """
    if normal_request(request)[0] is False:
        return HttpResponseRedirect('/service/index')
    params = request.POST.get('args', '')  # 爬取的参数
    type = request.POST.get('type', '')  # 请求的类型
    memo = request.POST.get('memo', '')

    if type not in ('baobao', 'role', 'equip'):
        return render_to_error_response(request, response, render, '错误的请求')
    try:
        _ = json.loads(params)
        pikle_params = _['params']
        pikle_service_options = _['option_params']
    except:
        return response_json('FAIL', msg="PARAMS_ERROR", description='上传的数据有误')
    service_time = pikle_service_options['service_time']  # 服务时间 day
    # 根据藏宝阁的规则转换参数

    service_name, crawl_url =  type_handle_func_dict[type](pikle_params, service_time)  # 不同爬取类型不同的处理

    # 处理服务参数
    push_type = ''
    if pikle_service_options.get('sms_notic'):
        push_type += '短信;'
    if pikle_service_options.get('email_notic'):
        push_type += '邮件'

    order = CrawlOrders.objects.create(oid='', uname=request.user.username, umobile=request.user.username,
                                       pay_status='待付款', memo=memo, service_name=service_name,
                                       user_id=request.user.id,
                                       user_ip=request.META.get('REMOTE_ADDR', ''),
                                       user_agent=request.META.get('HTTP_USER_AGENT'),
                                       status='待付款', create_time=render['timenow'],
                                       crawl_url=crawl_url, upload_params=params,
                                       first_round_push=pikle_service_options['first_round_push'],
                                       price_down_push=pikle_service_options['price_notic'],
                                       service_time=service_time,
                                       push_type=push_type,
                                       price=service_time * 100,
                                       real_price=service_time * 100,
                                    )
    return response_json(retcode='SUCC', msg='OrderCreate', description='订单创建成功', order_id=order.id)
    # 组织支付参数
    # 原来这里是form提交后直接返回页面的，但是这么做刷新或者后跳的效果不好 所有采用了重定向
    # return HttpResponseRedirect('/order/pay_page/%d' % order.id)
    # notify_url = '%s/order/order_paysapi_notify' % settings.RUN_URL
    # return_url = '%s/order/order_pay_success' % settings.RUN_URL
    # # 获取加密的order_oid和orderuid
    # prpcrypt_orderid = Prpcrypt.encrypt(order.id)
    # prpcrypt_orderuid = Prpcrypt.encrypt(order.user_id)
    # render['order'] = order
    # render['ali_payapi_post_params'] = paysapi_signature('%.2f' % (order.real_price / 100), 1, prpcrypt_orderid,
    #                                                      prpcrypt_orderuid, service_name, notify_url, return_url)
    # render['wx_payapi_post_params'] = paysapi_signature('%.2f' % (order.real_price / 100), 2, prpcrypt_orderid,
    #                                                     prpcrypt_orderuid, service_name, notify_url, return_url)
    # render['currency'] = '%.2f' % (request.user.userprofile.currency / 100)
    # return render_to_response(request, response, render, 'order/pay_page.html')
    # return HttpResponseRedirect('/order/pay_page/%s' % order.id)
    # 发布新的爬取url  todo 这里应该转到付款完成后  截至时间存放到redis中  设置ttl
    # 爬取的类型 bb, 爬取的url: _bb_crawl_url, 订单id: o.id, 订单备注: memo, 用户id: request.user.id
    # push_type: 推送的方式 first_round_push 第一轮推送 # 服务时间的截至时间: service_time
    # crawl_task.delay('bb', _crawl_url, {
    #     'order_id': order.id,
    #     'memo': memo,
    #     'user_id': request.user.id,
    #     'push_type': push_type,
    #     'service_time': datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(hours=2), '%Y-%m-%d %H:%M:%S'),
    #     'time_range': {'days': 1},
    #     'first_round_push': pikle_service_options['first_round_push'],
    #     'price_down_push': pikle_service_options['price_notic'],
    # })
    # return response_json(retcode='SUCC', msg='BB_START_CRAWL', description='请求成功')







