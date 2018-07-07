# encoding: utf-8
from django.conf.urls import include, url
from .views import *
urlpatterns = [
    url('^index/?$', index),  # 服务列表页面
    url('^service_page/(?P<type>召唤兽|装备|角色)/?$', service_page, {'need_login': True}), # 具体的每个服务选项页面
    url('^crawl_request/?$', crawl_request, {'need_login': True}),  # 发送服务请求
]
