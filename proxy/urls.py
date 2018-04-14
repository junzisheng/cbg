from django.conf.urls import include, url
from .in_proxy import *
from .out_proxy import *
from unit.utility import IProxyManager
p = IProxyManager()
urlpatterns = [
    url('^select/?$', select, {'IProxyManager': p}),
    url('^delete/?$', delete, {'IProxyManager': p}),
    url('^insert/?$', insert,  {'IProxyManager': p}),
]
