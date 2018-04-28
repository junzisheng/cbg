# encoding: utf-8
from django.conf.urls import include, url
from .views import *
urlpatterns = [
    url('^role/?$', role_page),
    url('^bb/?', bb_page),
    url('^role_crawl_url/?$', role_crawl_rul)
]
