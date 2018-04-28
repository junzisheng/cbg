from django.conf.urls import include, url
from .views import *
urlpatterns = [
    url('^index/?', index),
    url('^login/?$', login),
    url('^register/?$', register),
    url('^userreg/?$', userreg),
    url('^userlogin/?$', userlogin),
    url('^qrcode/?$', qrcode_),
    url('^checkcode_img', check_codeimage)
]
