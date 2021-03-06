# encoding=utf-8
from django.db import transaction

from order.models import CbgOrders, CbgOrderDetail
from service.models import CbgService
from service.functions import bb_params_handle, role_params_handel, equip_params_handel
from unit.utility import *
from unit.cache import RedisKeyCache
from unit.decoration import banner


type_handle_func_dict = {
    1: bb_params_handle,
    2: role_params_handel,
    3: equip_params_handel,
}


@banner()
def index(request, response, render):
    """服务列表页面"""
    return render_to_response(request, response, render, 'service/templates/index.html')


def service_page(request, response, render, service_id):
    """服务detail， type: 召唤兽|装备|角色"""
    render['service_id'] = service_id
    return render_to_response(request, response, render, 'service/templates/service.html')


def service_modify(request, response, render, order_id):
    """修改订单的参数"""
    try:
        order = CbgOrders.objects.get(id=order_id, is_delete=0)
    except CbgOrders.DoesNotExist:
        return render_to_error_response(request, response, render, '错误的订单号')
    if order.status not in ['待付款', '进行中']:
        return render_to_error_response(request, response, render, '只有待付款和进行中的状态可以修改参数哦！')
    if order.modify_times <= 0:
        return render_to_error_response(request, response, render, '该订单的修改次数已用完！')
    render['order'] = order
    render['service_id'] = order.service_id
    return render_to_response(request, response, render, 'service/templates/service.html')


@transaction.atomic
def service_modify_api(request, response, render, order_id):
    """订单修改参数"""
    upload_params = request.POST.get('params')
    memo = request.POST.get('memo', "")
    try:
        order = CbgOrders.objects.select_for_update().get(id=order_id, user_id=request.user.id, is_delete=0)
        order_detail = CbgOrderDetail.objects.get(order_id=order.id)
    except:
        return response_json(retcode="FAIL", msg="ErrorOid", description='错误的订单号！')
    try:
        params = json.loads(upload_params)
        public_params = params['public_params']
        private_params = params['private_params']['params']
        service_params = public_params['option_params']
        service = CbgService.objects.get(id=public_params['service_id'])
    except:
        return response_json('FAIL', msg="ErrorParams", description='上传的数据有误！')
    if order.modify_times <= 0:
        return response_json('FAIL', msg="MissModifyTimes", description='修改次数已用完！')
    service_time = service_params['service_time']  # 服务时间 day
    if order.status not in ['待付款', '进行中']:
        return response_json(retcode="FAIL", msg="ErrorStatus", description='错误的请求！')
    if service_time != order_detail.service_time and order.status == '进行中':
        return response_json('FAIL', msg="PARAMS_ERROR", description='错误的请求！')
    if not (1 <= service_time <= 30):
        return response_json('FAIL', msg="PARAMS_ERROR", description='上传的数据有误！')
    if order.status == '待付款':
        order_detail.service_time = service_time
        # todo 需要重新计算价格
    if order.status == '进行中':
        order.modify_times -= 1
    push_type = ""
    if service_params.get('sms_notic'):
        push_type += '短信;'
    if service_params.get('email_notic'):
        push_type += '邮件;'
    crawl_url =  type_handle_func_dict[service.id](private_params)  # 不同爬取类型不同的处理
    # 更新
    order_detail.crawl_url = crawl_url
    order_detail.first_round_push = service_params['first_round_push']
    order_detail.price_down = service_params['price_notic']
    order_detail.push_type = push_type
    order_detail.upload_params = upload_params
    service_info = '{push_type}|{service_time}|{first_push}|{price_push}|{memo}'.format(push_type=push_type,
                                                                                        service_time=service_time, first_push=service_params['first_round_push'],
                                                                                        price_push=service_params['price_notic'], memo=memo)
    order.price =  service_time * service.price
    order.service_id = service.id
    order.service_info = service_info
    order.last_modify_time = datetime.datetime.now()
    order.save()
    order_detail.save()
    # 修改爬取任务的参数
    if order.status == '进行中':
        pass
    # todo 记录表
    return response_json('SUCC', msg="OrderModifySucc", description='订单数据修改成功！', left_modify_times=order.modify_times)


@transaction.atomic
def crawl_request(request, response, render):
    """
    爬取请求
    """
    upload_params = request.POST.get('params')
    memo = request.POST.get('memo', "")
    try:
        params = json.loads(upload_params)
        public_params = params['public_params']
        private_params = params['private_params']['params']
        service_params = public_params['option_params']
        service = CbgService.objects.get(id=public_params['service_id'])
    except:
        return response_json('FAIL', msg="ParamsError", description='上传的数据有误')

    service_time = service_params['service_time']  # 服务时间 day
    if not (1 <= service_time <= 30):
        return response_json('FAIL', msg="ParamsError", description='上传的数据有误')
    # 根据藏宝阁的规则转换参数
    crawl_url =  type_handle_func_dict[service.id](private_params)  # 不同爬取类型不同的处理

    # 处理服务参数
    push_type = ''
    if service_params.get('sms_notic'):
        push_type += '短信;'
    if service_params.get('email_notic'):
        push_type += '邮件'
    service_info = '{push_type}|{service_time}|{first_push}|{price_push}|{memo}'.format(push_type=push_type,
                    service_time=service_time, first_push=service_params['first_round_push'],
                    price_push=service_params['price_notic'], memo=memo)
    order, is_new= CbgOrders.objects.get_or_create(
        status='初始状态',
        user_id=request.user.id,
        defaults=dict(
            service_name=service.name,
            service_id=service.id,
            price= service.price * service_time,
            pay_status='待付款',
            modify_times=3,
            create_time=render['timenow'],
            service_info=service_info,
        )
    )
    if is_new is False:
        order.service_name = service_time
        order.service_id = service.id
        order.price = service_time * 100
        order.pay_status = '待付款'
        order.modify_times = 3
        order.create_time = render['timenow']
        order.service_info = service_info
        order.save()
        CbgOrderDetail.objects.filter(order_id=order.id).update(
            order=order, memo=memo,
            user_ip=request.META.get('REMOTE_ADDR', ''), user_agent=request.META.get('HTTP_USER_AGENT'),
            crawl_url=crawl_url, upload_params=upload_params,
            first_round_push=service_params['first_round_push'],
            price_down_push=service_params['price_notic'],
            push_type=push_type,
            service_time=service_time,
        )
    else:
        CbgOrderDetail.objects.create(
            user_id=order.user_id, order=order, memo=memo,
            user_ip=request.META.get('REMOTE_ADDR', ''), user_agent=request.META.get('HTTP_USER_AGENT'),
            crawl_url=crawl_url, upload_params=upload_params,
            first_round_push=service_params['first_round_push'],
            price_down_push=service_params['price_notic'],
            push_type=push_type,
            service_time=service_time,
        )
    return response_json(retcode='SUCC', msg='OrderCreate', description='订单创建成功', order_id=order.id)








