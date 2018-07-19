"""cbg_backup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.conf import settings
from django.views import static
from order.views.data import crawl_data_page
from libraries import xadmin

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url('^d/(?P<order_id>\d+)/?$', crawl_data_page, {'need_login': True}),  # 爬取数据的页面 这里是为了减少短信的长度而作为根url
    url(r'^user/', include('user.urls')),
    url(r'^service/', include('service.urls')),
    url(r'^others/', include('others.urls')),
    url(r'^order/', include('order.urls')),
    url(r'^activity/', include('activity.urls')),
    url(r'^coupon/', include('coupon.urls')),
    url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}, name='static')  # setting.DEBUG is False
]

