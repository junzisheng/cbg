import datetime

from django.db import transaction
from django.http import HttpResponseRedirect

from coupon.models import CbgCouponUserRelation
from coupon.models import CbgCoupon
from coupon.functions import assigin_coupon
from unit.utility import render_to_response, response_json
from unit.decoration import ajax_refresh
from unit.utility import dtlib, obj_2_json
from unit.db_tools import run_custom_sql


def coupon_center(request, response, render):
    """领券中心"""
    # 获取所有能够领取的优惠券
    today = datetime.date.today()
    render['coupon_list'] = CbgCoupon.objects.filter(acquire_start_time__lte=today, acquire_end_time__gte=today, received=1)
    # 获取用户已经拥有的优惠券
    render['my_cp_list'] = []
    if request.user.is_authenticated:
        my_coupons = CbgCouponUserRelation.objects.filter(user_id=request.user.id)
        render['my_cp_list'] = [_x.coupon_id for _x in my_coupons]
    return render_to_response(request, response, render, 'coupon/templates/coupon_center.html')


def my_coupon_page(request, response, render):
    return render_to_response(request, response, render, 'coupon/templates/my_coupon.html')


@ajax_refresh(order_limit=('-id',))
def my_coupon_api(request, response, render, status):
    today = render['timenow'].date()
    offset, order_by, int_limit, _ = render['query_params']
    filter_ = {'user_id': request.user.id}
    if status == 'wait':  # 未使用
        filter_['usage_time__isnull'] = True
        filter_['expire_time__gte'] = today
        filter_['status'] = 0  # 有订单占用未释放的情况
    elif status == 'already':   # 已使用
        filter_['usage_time__isnull'] = False
        filter_['status'] = 2
    elif status == 'expire':   # 已过期
        filter_['expire_time__lt'] = today
        # filter_['usage_time__isnull'] = True
        filter_['status__in'] = (0, 1)
    queryset = CbgCouponUserRelation.json_queryset(order_by=order_by, offset=offset, limit=int_limit, filter_=filter_)
    if queryset:
        cp_id_list = [_x['coupon_id'] for _x in queryset]
        # 查询优惠券信息
        cp_list = CbgCoupon.objects.filter(id__in=cp_id_list)
        cp_dict = dict((_x.id, _x) for _x in cp_list)
        for _query in queryset:
            _cp = cp_dict.get(_query['coupon_id'])
            if _cp:
                can_use = today <= dtlib.FMT2(_query['expire_time']) and _query['status'] == 0 # 是否可以立即使用
                _query.update({'style':_cp.style, 'fill': _cp.fill, 'discount': _cp.discount, 'reduction': _cp.reduction,
                               'acquire_end_time': dtlib.FDD3(_cp.acquire_end_time),
                               'acquire_start_time': dtlib.FDD3(_cp.acquire_start_time),
                               'service_range': _cp.service_range,
                               'current_use': can_use})
    return {'query_list': queryset}


@transaction.atomic
def get_coupon_api(request, response, render, coupon_id):
    """领取优惠券的api"""
    ret_code, err_txt = assigin_coupon(request.user, coupon_id, "")
    return response_json(retcode="SUCC" if ret_code == 0 else 'FAIL', description=err_txt )


def use_coupon_redirect(request, response, render, coupon_id):
    """使用优惠券"""
    sql = 'select cbgservice_id from cbg_coupon_service where cbgcoupon_id=%s'
    res, _ = run_custom_sql(sql, coupon_id)
    service_id_list = [_x[0] for _x in res]
    # todo 是否可以不用重定向
    if len(service_id_list) == 1:
        return HttpResponseRedirect('/service/service_page/%s' % service_id_list[0])
    else:
        return HttpResponseRedirect('/service/index')


def get_service_coupon_api(request, response, render, service_id):
    """获取某个活动可用优惠券的接口"""
    today = render['timenow'].date()
    # 1. 获取用户拥有的所有优惠券
    my_coupon_list = CbgCouponUserRelation.objects.filter(user_id=request.user.id, status=0,
                                             acquire_time__lte=today, expire_time__gte=today, usage_time__isnull=True)
    if not my_coupon_list:
        return response_json(retcode='SUCC', result='[]')
    # 2. 获取这些优惠券使用的service
    my_coupon_id_list = [str(_c.coupon_id) for _c in my_coupon_list]
    # 3. 筛选目标优惠券
    sql = 'select cbgcoupon_id from cbg_coupon_service where cbgcoupon_id in (' + ','.join(my_coupon_id_list) +') and cbgservice_id=%s'
    res, _ = run_custom_sql(sql, service_id)
    vaild_coupon_id_list = [_x[0] for _x in res]
    if not vaild_coupon_id_list:
        return response_json(retcode='SUCC', queryset='[]')
    vaild_my_coupon_list = [_c for _c in my_coupon_list if _c.coupon_id in vaild_coupon_id_list]
    vaild_my_coupon_dict = dict((_x.coupon_id, _x) for _x in vaild_my_coupon_list)
    # 4. 获取目标优惠券的信息
    coupon_list = CbgCoupon.objects.filter(id__in=vaild_coupon_id_list)
    # 5. 组装优惠券的信息
    result = []
    for coupon in coupon_list:
        my_rel = vaild_my_coupon_dict.get(coupon.id)
        if my_rel:
            r = obj_2_json(my_rel,support_json=True)
            r.update(obj_2_json(coupon, support_json=True))  # 奖券的过期时间是按relation中来算 不安coupon来算 因为有的券的过期时间是从领取后计算的
            r['id'] = my_rel.id
            result.append(r)
    return response_json(retcode='SUCC', result=result)






