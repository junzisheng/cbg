# encoding: utf-8
from django.conf.urls import url
from .views import *
urlpatterns = [
    url('^mine/?', mine, {'need_login': True}),  # 个人中心
    url('^login/?$', login, {'check_active': False}),
    url('^register/?$', register, {'check_active': False}),
    url('^userreg/?$', userreg, {'check_active': False}),
    url('^userlogin/?$', userlogin, {'ajax': True, 'check_active': False}),
    url('^userlogout/?$', userlogout, {'need_login': True}),
    url('^settings/?$', settings_page, {'need_login': True}),
    url('^info/?$', info, {'need_login': True}),
    url('^info_save/?$', info_save, {'need_login': True}),
    url('^modify_pwd/?$', modify_pwd_page, {'need_login': True}),
    url('^modify_pwd_api/?$', modify_pwd_api, {'need_login': True}),
    url('^qrcode/?$', qrcode_),  # 二维码
    url('^checkcode_img/?$', check_codeimage),  # 认证吗
    url('^send_captcha/?$', send_captcha), # 发送手机短信验证码
    url('^message_page/?$', message_page, {'need_login': True}),
    url('^get_message/?$', get_message_api, {'need_login': True}),
    url('^sign/?$', sign_api, {'need_login': True}),  # 用户签到
]
