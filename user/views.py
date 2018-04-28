from django.shortcuts import render
import re
from io import BytesIO
import qrcode
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse
from unit import gpub
from unit.utility import render_to_response, ip_visit_limit, response_json, validate_nick_name
from unit.functions import *
from .models import UserProfile

@gpub.wglobal(allow_tuple=('GET', 'POST'))
def index(request, response, _render):
    if request.user.is_authenticated():
        return HttpResponse('已登陆')
    return HttpResponse('未登陆')



@gpub.wglobal(allow_tuple=('GET',))
def login(request, response, _render):
    return render_to_response(request, response, _render, 'auth/login.html')


@gpub.wglobal(allow_tuple=('GET',))
def register(request, response, _render):
    return render_to_response(request, response, _render, 'auth/register.html')


@gpub.wglobal(allow_tuple=('POST'))
def userreg(request, response, render):
    username = request.POST.get('username', '')
    password = request.POST.get('pwd', '')
    checkcode = request.POST.get('checkcode', '')
    # nickname = request.POST.get('nickname', '')
    # 校验账号
    if ' ' in username:
        return response_json(retcode='FAIL', msg='USERNMAE_UNAVAILABLE', description='账号不能含有空格！')
    if not 6 <= len(username) <= 12:
        return response_json(retcode='FAIL', msg='USERNAME_UNAVAILABLE', description='账号必须在6-12位之间！')
    # 校验密码
    if not 6 <= len(password) < 16:
        return response_json(retcode='FAIL', msg='PASS_UNAVAILABLE', description='密码必须在6-16位之间！')
    if checkcode != request.session.get('checkcode'):
        return response_json(retcode='FAIL', msg='CHECKCODE_ERROR', description='验证码错误！')
    if 'checkcode' in request.session:
        del request.session['checkcode']
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
        return response_json(retcode='FAIL', msg="USER_EXIST", description='该账号已被注册')

    # 创建用户
    user = User.objects.create_user(username = username, email = '', password = password)
    user.save()
    UserProfile.objects.create(nickname=username, user_id=user.id)
    return response_json(retcode='SUCC', msg='SUCCESS', description='注册成功！')


@gpub.wglobal(allow_tuple=('POST',), ajax=True)
def userlogin(request, response, _render):
    user_ip = request.META.get('REMOTE_ADDR' , '')
    redirect = request.POST.get('redirect', '/user/index')
    # todo 放在中间件中
    if ip_visit_limit(user_ip , 'login' , 10, 60):
        return response_json(retcode='FAIL', msg="IP_LIMIT", description="您的访问过于频繁，请稍后重试")
    username = request.POST.get('username', '')
    pwd = request.POST.get('pwd', '')
    user = auth.authenticate(username=username, password=pwd)
    if not user:
        return response_json(retcode='FAIL' , msg = 'WRONG_USER' ,description = u'手机号或密码错误!' )
    auth.login(request, user)
    if request.POST.get('auto_login') == 'true':
        request.session.set_expiry(60 * 60 * 24 * 14)
    else:
        request.session.set_expiry(0)
    return response_json(retcode='SUCC' , msg='LOGIN_SUCC', redirect=redirect)


@gpub.wglobal(allow_tuple=('GET',))
def qrcode_(request, response, _render):
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


@gpub.wglobal(allow_tuple=('GET',))
def check_codeimage(request, response, render):
    """ 获取图形验证码 """
    code_img = create_validate_code()
    request.session['checkcode'] = code_img[1].lower()
    buf = BytesIO()
    code_img[0].save(buf, "GIF")
    return HttpResponse(buf.getvalue(),'image/gif')


