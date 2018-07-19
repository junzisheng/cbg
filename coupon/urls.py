from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'coupon_center/?$', coupon_center),
    url(r'my_coupon/?$', my_coupon_page, {'need_login': True}),
    url(r'my_coupon_api/(?P<status>wait|already|expire)/?$', my_coupon_api, {'need_login': True}),  # 获取个人优惠券的信息 未使用|已使用|已过期
    url(r'get_coupon_api/(?P<coupon_id>\d+)/', get_coupon_api, {'need_login': True}),  # 获取个人优惠券的信息 未使用|已使用|已过期
    url(r'use_coupon_redirect/(?P<coupon_id>\d+)/', use_coupon_redirect, {'need_login': True}),  # 获取个人优惠券的信息 未使用|已使用|已过期
    url(r'get_service_coupon_api/(?P<service_id>\d+)/', get_service_coupon_api, {'need_login': True})  # 获取个人优惠券的信息 未使用|已使用|已过期
]
