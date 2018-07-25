import random
import datetime
from django.db import transaction
from user.models import UserProfile
from order.models import CbgRechargeRecord
from coupon.models import CbgCoupon
from unit.utility import render_to_response, response_json, render_to_error_response
from .models import CbgLottery1, CbgConvertCode, CbgConvertCodeLog
from coupon.functions import assigin_coupon


@transaction.atomic
def index(request, response, render):
    """抽奖的首页"""
    return render_to_response(request, response, render, 'activity/templates/index.html')


@transaction.atomic
def turnplate_begin(request, response, render):
    """转盘开始抽奖"""
    today = render['timenow'].date()
    rd = random.randint(1, 100)  # 随机取1-100
    # code = 2
    code = 7
    # 谢谢参与 30%
    res_code, error_txt = assigin_coupon(request.user, random.randint(1,2), '', auto_expire=datetime.timedelta(days=3))
    if res_code == 0:
        try:
            lottery = CbgLottery1.objects.select_for_update().get(user=request.user, last_lottery_time=today)
            lottery.lottery_times -= 1
            lottery.save()
        except CbgLottery1.DoesNotExist:
            return response_json(retcode='FAIL', msg='UnLegalVist', description='非法访问')
        return response_json(retcode='SUCC', msg="TurplateSucc", code=code, left_times=lottery.lottery_times)
    else:
        return response_json(retcode='FAIL', msg=res_code, description=error_txt)


    if 1 <= rd <= 30:
        code = 2
    # 10盒币 5%
    elif 31 <= rd <= 35:
        code = 0
    # 5盒币 10
    elif 36 <= rd <= 45:
        code = 3
    # 1盒币 15%
    elif 46 <= rd <= 60:
        code = 8
    # 10积分  5%
    elif 61 <= rd <= 65:
        code = 1
    # 5积分 10%
    elif 66 <= rd <= 75:
        code = 9
    # 1积分  15%
    elif 76 <= rd <= 90:
        code = 6
    # 优惠券1
    elif 91 <= rd <= 95:
        code = 4
    # 优惠券2
    elif 95 <= rd <= 100:
        code = 7
    return response_json(retcode='SUCC', msg="TurplateSucc", code=code)


def use_convert_page(request, response, render):
    """使用兑换码"""
    return render_to_response(request, response, render, 'activity/templates/convert_page.html')


@transaction.atomic
def use_convert_api(request, response, render):
    code = request.GET.get('code', '')
    if len(code) != 36:
        return response_json(retcode='FAIL', msg='ErrorConvertCode', description='错误的兑换码！')
    try:
        convert = CbgConvertCode.objects.select_for_update().get(convert_code=code)
    except:
        return response_json(retcode='FAIL', msg='ErrorConvertCode', description='错误的兑换码！')
    if convert.receive_total >= convert.total_limit:
        return response_json(retcode='FAIL', msg='ConvertQuantityLimit', description='该兑换码已被领完！')
    if CbgConvertCodeLog.objects.filter(user=request.user, convert=convert).count() >= convert.quantity_limit:
        return response_json(retcode='FAIL', msg='ConvertUserLimig', description='您已兑换过！')
    if render['timenow'] > convert.end_time:
        return response_json(retcode='FAIL', msg='ConvertDeadline', description='该兑换码已过期！')
    if render['timenow'] < convert.start_time:
        return response_json(retcode='FAIL', msg='ConvertFuture', description='该兑换码未到领取时间！')
    # 货币奖励

    content =""
    if convert.obj_type == 2:
        profile = UserProfile.objects.select_for_update().get(user_id=request.user.id)
        CbgRechargeRecord.objects.create(user=request.user, quantity=convert.obj_quantity, give=0, status='已支付',
                                         left_quantity=profile.currency, create_time=render['timenow'],
                                         pay_time=render['timenow'], alias='兑换码')
        profile.currency += convert.obj_quantity
        profile.save()
        CbgConvertCodeLog.objects.create(user=request.user, convert=convert)
        content = "恭喜您，成功兑换到了%s个货币" % (convert.obj_quantity / 100.0)
    # 发放优惠券
    elif convert.obj_type == 1:
        b, error = assigin_coupon(request.user, convert.obj_id, '', datetime.timedelta(days=7))
        if b != 0:
            return response_json(retcode='FAIL', msg='ConvertCouponFail', description=error)
        coupon = CbgCoupon.objects.get(id=convert.obj_id)
        content = "恭喜您，成功兑换到了【%s】" % coupon.coupon_name
    convert.receive_total += 1
    convert.save()
    return response_json(retcode='SUCC', msg='ConvertSucc', content=content)






