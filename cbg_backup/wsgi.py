"""
WSGI config for cbg_backup project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import types
import sys

from importlib import import_module
from django.core.wsgi import get_wsgi_application

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 载入setting
from cbg_backup import settings
from share.setting_share import env
# run_setting = 'ecs' if env in ('ali_1', 'ali_2') else 'localhost'
# setting_module = import_module('setting.%s' % run_setting)
# for k in dir(setting_module):
#     if k.startswith('__'):
#         continue
#     v = getattr(setting_module, k)
#     if not isinstance(v, types.ModuleType):
#         setattr(settings, k, v)

# from django.core.management import execute_from_command_line
from jinja2 import Environment, FileSystemLoader
templates_dirs = [os.path.join(settings.BASE_DIR, 'templates')]
jinja2_env = Environment(loader = FileSystemLoader(templates_dirs), trim_blocks=True)
from cbg_backup import filters
for k in dir(filters):
    v = getattr(filters, k)
    if k not in ['contextfilter'] and not k.startswith('_') and isinstance(v, types.FunctionType):
        if k in jinja2_env.filters:
            print('警告：过滤器%s已经在%s中定义了' % (k, k.__module__))
        jinja2_env.filters[k] = v

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cbg_backup.settings")

application = get_wsgi_application()
