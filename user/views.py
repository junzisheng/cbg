import datetime
from io import BytesIO
import qrcode

from django.contrib import auth
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt

from cbg_backup.filters import get_wait_message
from unit.utility import render_to_response, response_json, del_session_key
from unit.functions import *
from .functions import send_ali_sms
from .models import UserProfile, CbgSysInfo, CbgUserSign
from order.models import CbgRechargeRecord
from activity.models import CbgLottery1

from coupon.models import CbgCouponUserRelation
from unit.decoration import sms_check
from unit.decoration import ajax_refresh


def login(request, response, render):
    render['redirect'] = request.GET.get('redirect', '/user/mine')
    return render_to_response(request, response, render, 'auth/login.html')


def register(request, response, render):
    return render_to_response(request, response, render, 'auth/register.html')


@csrf_exempt
@transaction.atomic
def userreg(request, response, render):
    username = request.POST.get('username', '')
    password = request.POST.get('pwd', '')
    captcha = request.POST.get('captcha', '')
    # nickname = request.POST.get('nickname', '')
    # 校验账号
    if len(username) != 11 or not username.isdigit():
        return response_json(retcode='FAIL', msg='UsernamaError', description='账号必须在6-12位之间！')
    # 校验密码
    if not 6 <= len(password) < 16:
        return response_json(retcode='FAIL', msg='PwdError', description='密码必须在6-16位之间！')
    if len(captcha) != 4 or (captcha.encode() != settings.redis3.get('register_captcha_%s' % username)):
        return response_json(retcode='FAIL', msg='CatpchaError', description='验证码错误')
    # if checkcode != request.session.get('checkcode'):
    #     return response_json(retcode='FAIL', msg='CHECKCODE_ERROR', description='验证码错误！')
    # if 'checkcode' in request.session:
    #     del request.session['checkcode']
    # 校验昵称
    # 1.规范性
    # nickname = re.sub(u"[^\u0000-\uffff]", u"", nickname)
    # msg = validate_nick_name(nickname)
    # if msg:
    #     return response_json(retcode='FAIL', msg="NICKNAME_UNAVAILABLE", description=msg)
    # 2.唯一性
    # if UserProfile.objects.filter(nickname=nickname).exists():
    #     return response_json(retcode='FAIL', msg="NICKNAME_REPEAT", description='该昵称已被占用，请更换其它昵称。')
    # 校验验证码
    # if captcha != gpub.redis3.get("captcha_%s" % username):
    #     return response_json(retcode='FAIL', msg='CAPTCHA', description='手机验证码错误！')
    # gpub.redis3.delete("captcha_%s" % username)
    # 用户是否已经注册
    if User.objects.filter(username=username).exists():
        return response_json(retcode='FAIL', msg="UserExist", description='该账号已被注册')
    # 创建用户
    user = User.objects.create_user(username=username, email='', password=password)
    user.save()
    UserProfile.objects.create(nickname=username, user_id=user.id)
    # 删除验证码
    settings.redis3.delete("register_captcha_%s" % username)
    return response_json(retcode='SUCC', msg='SUCCESS', description='注册成功！')


def userlogin(request, response, render):
    user_ip = request.META.get('REMOTE_ADDR' , '')
    # redirect = request.POST.get('redirect', '/user/index')
    # todo 放在中间件中
    # if ip_visit_limit(user_ip , 'login' , 10, 60):
    #     return response_json(retcode='FAIL', msg="IP_LIMIT", description="您的访问过于频繁，请稍后重试")
    username = request.POST.get('username', '')
    pwd = request.POST.get('pwd', '')
    user = auth.authenticate(username=username, password=pwd)
    if not user:
        return response_json(retcode='FAIL', msg = 'WRONG_USER' ,description = u'手机号或密码错误!' )
    auth.login(request, user)
    if request.POST.get('auto_login') == 'true':
        request.session.set_expiry(60 * 60 * 24 * 14)
    else:
        request.session.set_expiry(0)
    # 查看是否有通知， 给用户进行通知
    # 1. 检查消息中心  这个在模板中通过过滤器获取到了
    # render['notic_list'] = []
    # # 2. 检查是否有新的通知
    # sys_count = get_wait_message(request.user.id, 'all')
    # if sys_count:
    #     render['notic_list'].append({
    #         'title': '您的消息中心有%s条新的消息未查看' % sys_count,
    #         'desc': "",
    #     })
    return response_json(retcode='SUCC' , msg='LOGIN_SUCC')


def userlogout(request, response, render):
    """用户注销"""
    auth.logout(request)
    return HttpResponseRedirect('/user/login')


def settings_page(request, response, render):
    return render_to_response(request, response, render, 'user/templates/setting/index.html')


def modify_pwd_page(request, response, render):
    return render_to_response(request, response, render, 'user/templates/setting/change_pwd.html')


def modify_pwd_api(request, response, render):
    captcha = request.POST.get('captcha', '')
    new_pwd = request.POST.get('new_pwd', '')
    if  not (6 <= len(new_pwd) <= 16):
        return response_json(retcode='FAIL', msg='UnLegalPwd', description='密码格式错误！')
    if len(captcha) != 4 or (captcha.encode() != settings.redis3.get('modify_pwd_captcha_%s' % request.user.username)):
        return response_json(retcode='FAIL', msg='CatpchaError', description='验证码错误！')
    settings.redis3.delete("modify_pwd_captcha_%s" % request.user.username)
    request.user.set_password(new_pwd)
    request.user.save()
    auth.logout(request)
    return response_json(retcode='SUCC', msg='ModifyPwdSuccess', description='密码修改成功！')


def mine(request, response, render):
    """个人中心"""
    today = datetime.date.today()
    render['valid_coupons'] =  CbgCouponUserRelation.objects.filter(user_id=request.user.id, status=0,
                                         expire_time__gte=today, usage_time__isnull=True).count()
    # 今日是否签到过
    render['has_signed'] = CbgUserSign.objects.filter(user=request.user, sign_time=render['timenow'].date())
    # 获取今日抽奖剩余次数
    return render_to_response(request, response, render, 'auth/mine.html')


def qrcode_(request, response, render):
    """二维码"""
    data = request.GET.get('data')
    qr = qrcode.QRCode(version=1, error_correction=qrcode.ERROR_CORRECT_L, box_size=5, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()
    mio = BytesIO()
    img.save(mio, 'png')
    mio.seek(0)
    response['Content-Type'] = 'image/png'
    response.write(mio.read())
    return response


def check_codeimage(request, response, render):
    """ 获取图形验证码 """
    code_img = create_validate_code()
    # todo prefix
    request.session['checkcode'] = code_img[1].lower()
    buf = BytesIO()
    code_img[0].save(buf, "GIF")
    return HttpResponse(buf.getvalue(), 'image/gif')


@sms_check('username', 300 - 60)
def send_captcha(request, response, render, username=""):
    """获取短信验证码"""
    type = request.GET['type']
    captcha = ""
    if type == 'register':
        if User.objects.filter(username=username):
            return response_json('FAIL', description='该手机号已被注册', msg='HasRegistered')
        # 校验图形验证码
        if request.session.get('checkcode', '-1') != request.GET.get('checkcode', '-2'):
            return response_json('FAIL', description='验证码错误', msg='ErrorCheckCode')
        del_session_key(request.session, 'checkcode')
        captcha = send_ali_sms(username, type)
    elif type == 'currency_pay':
        captcha = send_ali_sms(username, type)
    elif type == 'modify_pwd':
        captcha = send_ali_sms(username, type)
    else:
        return response_json('FAIL', description='错误的请求！', msg='UnlegalRequest')
    captcha = captcha if request.user.is_superuser == 1 else ""
    return response_json('SUCC', description='注册码已发送', msg='SendSucc', captcha=captcha)


def message_page(request, response, render):
    """消息通知界面"""
    return render_to_response(request, response, render, 'user/templates/message/index.html')


@ajax_refresh(order_limit=('-id',), filter_limit={'type_1': 'notic|offer'})
def get_message_api(request, response, render):
    """获取消息的接口"""
    offset, order_by, int_limit, filter_ = render['query_params']
    settings.redis3.hset('user_message', '%s:%s' % (filter_['type'], request.user.id), 0)
    filter_['user_id__in'] = [0, request.user.id]  # 0: 系统消息
    filter_['display_time__lte'] = render['timenow']
    queryset = CbgSysInfo.json_queryset(order_by=order_by, offset=offset, limit=int_limit, filter_=filter_)
    return {'query_list': queryset}


@transaction.atomic
def sign_api(request, response, render):
    today = render['timenow'].date()
    sign_log = CbgUserSign.objects.filter(user_id=request.user.id)
    if sign_log:
        sign_log = sign_log[0]
        if sign_log.sign_time == today:
            return response_json(retcode='FAIL', msg='SignRepeat', description='请不要重复签到！')
        # 计算连续多久签到了
        if today - sign_log.sign_time == datetime.timedelta(days=1):
            sign_log.continue_days += 1
        else:
            sign_log.continue_days = 1
        sign_log.last_sign_time = sign_log.sign_time
        sign_log.sign_time = today
        sign_log.save()
    else:
        sign_log = CbgUserSign.objects.create(user=request.user, sign_time=today, last_sign_time=today, continue_days=1)
    # 签到奖励
    # 1. 盒币奖励
    profile = UserProfile.objects.select_for_update().get(user=request.user)
    prize_currency = 100 if sign_log.continue_days < 7 else 200
    CbgRechargeRecord.objects.create(user=request.user, quantity=prize_currency, give=0, status='已支付',
             left_quantity=profile.currency, create_time=render['timenow'], pay_time=render['timenow'], alias='签到')
    profile.currency += prize_currency
    profile.save()
    # 抽奖次数奖励
    lotter = CbgLottery1.objects.select_for_update().filter(user=request.user)
    if not lotter:
        CbgLottery1.objects.create(lottery_times=3+3, last_lottery_time=today, user=request.user)
    else:
        lotter = lotter[0]
        if lotter.last_lottery_time == today:
            lotter.lottery_times += 3
        else:
            lotter.lottery_times = 3 + 3
            lotter.last_lottery_time = today
        lotter.save()
    return response_json(retcode='SUCC', msg='SignSucc', description='签到成功！', continue_days=sign_log.continue_days,
                         prize_currency=prize_currency, prize_logger_times=3)













