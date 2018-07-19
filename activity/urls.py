from django.conf.urls import url
from .views import *

urlpatterns = [
    # 公共接口
    url('^index/?$', index, {'need_login': True}),
    url('^turnplate_begin/?$', turnplate_begin, {'need_login': True})
]
