# encoding: utf-8
from django.conf.urls import url
from .views import *
urlpatterns = [
    url('^mine/?', mine, {'need_login': True}),  # 个人中心
    url('^login/?$', login, {'check_active': False}),
    url('^register/?$', register, {'check_active': False}),
    url('^userreg/?$', userreg, {'check_active': False}),
    url('^userlogin/?$', userlogin, {'ajax': True, 'check_active': False}),
    url('^qrcode/?$', qrcode_),  # 二维码
    url('^checkcode_img/?$', check_codeimage),  # 认证吗
    url('^send_captcha/?$', send_captcha), # 发送手机短信验证码
    # url('^mine/?', mine, ),
    # url('^login/?$', login,),
    # url('^register/?$', register, ),
    # url('^userreg/?$', userreg),
    # url('^userlogin/?$', userlogin),
    # url('^qrcode/?$', qrcode_),  # 二维码
    # url('^checkcode_img/?$', check_codeimage),  # 认证吗
    # url('^send_captcha/?$', send_captcha), # 发送手机短信验证码
]
