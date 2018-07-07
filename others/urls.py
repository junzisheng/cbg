from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^bug_submit_page/?$', bug_submit_page),
    url(r'^submit_problems/?$', submit_problems, {'ajax': True}),
]
