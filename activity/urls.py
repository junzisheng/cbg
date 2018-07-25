from django.conf.urls import url
from .views import *

urlpatterns = [
    # 公共接口
    url('^index/?$', index, {'need_login': True}),
    url('^turnplate_begin/?$', turnplate_begin, {'need_login': True}),
    url('^convert_code_page/?$', use_convert_page, {'need_login': True}),  # 使用兑换码
    url('^use_convert_code_api/?$', use_convert_api, {'need_login': True}),  # 使用兑换码
]
