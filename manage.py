#!/usr/bin/env python
import os
import sys
from importlib import import_module
import types

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cbg_backup.settings")

    run_setting = None
    # 载入setting
    from cbg_backup import settings
    # from share.setting_share import env
    # run_setting = 'ecs' if env in ('ali_1', 'ali_2') else 'localhost'
    # setting_module = import_module('setting.%s' % run_setting)
    # for k in dir(setting_module):
    #     if k.startswith('__'):
    #         continue
    #     v = getattr(setting_module, k)
    #     if not isinstance(v, types.ModuleType):
    #         setattr(settings, k, v)
    from django.core.management import execute_from_command_line
    from jinja2 import Environment, FileSystemLoader
    templates_dirs = [os.path.join(settings.BASE_DIR, 'templates')]
    jinja2_env = Environment(loader=FileSystemLoader(templates_dirs) , trim_blocks = True)
    from cbg_backup import filters
    for k in dir(filters):
        v = getattr(filters, k)
        if k not in ['contextfilter'] and not k.startswith('_') and isinstance(v, types.FunctionType):
            if k in jinja2_env.filters:
                print('警告：过滤器%s已经在%s中定义了' % (k, k.__module__))
            jinja2_env.filters[k] = v
    execute_from_command_line(sys.argv)
