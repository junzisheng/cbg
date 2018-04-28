from django.conf.urls import include, url
from .views import *
from unit.utility import IProxyManager
p = IProxyManager()
urlpatterns = [
    url('^proxy_select/?$', select, {'IProxyManager': p}),
    url('^proxy_delete/?$', delete, {'IProxyManager': p}),
    url('^proxy_insert/?$', insert,  {'IProxyManager': p}),
]
