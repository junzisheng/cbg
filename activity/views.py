import random
import datetime
from django.db import transaction
from coupon.models import CbgCoupon
from unit.utility import render_to_response, response_json, render_to_error_response
from .models import CbgLottery1
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






