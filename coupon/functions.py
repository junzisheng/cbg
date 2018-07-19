import datetime

from coupon.models import CbgCouponUserRelation, CbgCoupon
from user.models import CbgSysInfo
from cbg_backup import settings
from unit.utility import obj_2_json
from unit.db_tools import run_custom_sql


def assigin_coupon(user, coupon_id, sys_txt, auto_expire=False):
    """发放优惠券,
    auto_expire: 是否根据当前时间生成优惠券的过期时间
    """
    now = datetime.datetime.now()
    today = datetime.date.today()
    try:
        coupon = CbgCoupon.objects.select_for_update().get(id=coupon_id, received=1)
    except:
        return -1, '错误的优惠券id'
    # 1 校验领取数量和时间
    if coupon.total_limit and coupon.acquire_count >= coupon.total_limit:
        return -2, '该优惠券已被领完！'
    if coupon.acquire_start_time > today:
        return -4, '未到领取时间!'
    if auto_expire is False and coupon.acquire_end_time < today:
        return -5, '已经过了领取时间!'
    # 2.校验这个优惠券每个用户可以领取的次数
    if coupon.assign_limit != 0 and coupon.assign_limit <= \
            CbgCouponUserRelation.objects.filter(user=user, coupon=coupon).count():
        return -3, '每人最多只能领取%s个' % coupon.assign_limit
    # 3. 插入到关系表中
    # 或者这个优惠券的可用范围
    service_id_list = coupon.service.all().values_list('id', flat=True)
    service_ids = ','.join([str(_id) for _id in service_id_list])
    expire_time = coupon.acquire_end_time if auto_expire is False else coupon.acquire_end_time + auto_expire
    CbgCouponUserRelation.objects.create(user_id=user.id, status=0, coupon=coupon, acquire_time=now, service_ids=service_ids,
                                         expire_time=expire_time)
    # 4. 记录优惠券的领取数
    coupon.acquire_count += 1
    coupon.save()
    # 5. 发送用户通知
    CbgSysInfo.objects.create(user=user, content='【%s】已经发放到您的账户中，请您查收' % coupon.coupon_name,
                              href="/coupon/my_coupon", display_time=now, type='notic')
    settings.redis3.hincrby('user_message', '%s:%s' % ('notic', user.id))
    return 0, ""


def get_user_service_coupon(request, service_id, order=None):
    today = datetime.date.today()
    # 1. 获取用户拥有的所有优惠券
    my_coupon_list = list(CbgCouponUserRelation.objects.filter(user_id=request.user.id, status=0, acquire_time__lte=today,
                                                               expire_time__gte=today))
    if not my_coupon_list:
        return []
    # 获取该服务能够使用的优惠券
    vaild_my_coupon_list = []
    for my_coupon in my_coupon_list:
        service_id_list = my_coupon.service_ids.split(',')
        if str(service_id) in service_id_list:
            vaild_my_coupon_list.append(my_coupon)
    vaild_my_coupon_dict = dict((_x.coupon_id, _x) for _x in vaild_my_coupon_list)
    # 4. 获取目标优惠券的信息
    coupon_list = CbgCoupon.objects.filter(id__in=[_x.coupon_id for _x in vaild_my_coupon_list])
    # 5. 组装优惠券的信息
    result = []
    for coupon in coupon_list:
        my_rel = vaild_my_coupon_dict.get(coupon.id)
        if my_rel:
            r = obj_2_json(my_rel,support_json=True)
            r.update(obj_2_json(coupon, support_json=True))
            r['id'] = my_rel.id
            result.append(r)
    return result


def check_coupoon_vaild(user, coupon):
    pass





