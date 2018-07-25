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
    from django.core.management import execute_from_command_line
    from jinja2 import Environment, FileSystemLoader
    templates_dirs = [os.path.join(settings.BASE_DIR, 'templates')]
    jinja2_env = Environment(loader=FileSystemLoader(templates_dirs) , trim_blocks = True)
    from cbg_backup import filters
    # 动态绑定filter到jinja中
    for k in dir(filters):
        v = getattr(filters, k)
        if k not in ['contextfilter'] and not k.startswith('_') and isinstance(v, types.FunctionType):
            if k in jinja2_env.filters:
                print('警告：过滤器%s已经在%s中定义了' % (k, k.__module__))
            jinja2_env.filters[k] = v
    execute_from_command_line(sys.argv)
