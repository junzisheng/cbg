# encoding: utf-8
from django.conf.urls import include, url
from .views import *
urlpatterns = [
    url('^index/?$', index),  # 服务列表页面
    url('^service_page/(?P<service_id>1|2|3)/?$', service_page, {'need_login': True}), # 具体的每个服务选项页面
    url('^service_modify/(?P<order_id>\d+)/?$', service_modify, {'need_login': True}), # 具体的每个服务选项页面
    url('^service_modify_api/(?P<order_id>\d+)/?$', service_modify_api, {'need_login': True}), # 具体的每个服务选项页面
    url('^crawl_request/?$', crawl_request, {'need_login': True}),  # 发送服务请求
]
