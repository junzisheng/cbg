from io import BytesIO
import qrcode
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from unit import gpub
from unit.utility import render_to_response, response_json, del_session_key
from unit.functions import *
from .functions import send_ali_sms
from .models import UserProfile
from unit.decoration import sms_check, sms_send


def login(request, response, render):
    render['redirect'] = request.GET.get('redirect', '/user/mine')
    return render_to_response(request, response, render, 'auth/login.html')


@sms_send
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
    return response_json(retcode='SUCC' , msg='LOGIN_SUCC')


@gpub.wglobal(allow_tuple=('GET',))
def mine(request, response, render):
    """个人中心"""
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
    if type == 'register':
        if User.objects.filter(username=username):
            return response_json('FAIL', description='该手机号已被注册', msg='HasRegistered')
        # 校验图形验证码
        if request.session.get('checkcode', '-1') != request.GET.get('checkcode', '-2'):
            return response_json('FAIL', description='验证码错误', msg='ErrorCheckCode')
        del_session_key(request.session, 'checkcode')
        send_ali_sms(username, type)
        return response_json('SUCC', description='注册码已发送', msg='SendSucc')
    elif type == 'currency_pay':
        send_ali_sms(username, type)
        return response_json('SUCC', description='注册码已发送', msg='SendSucc')







