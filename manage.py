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
    if '--env' in sys.argv:
        pos_env = sys.argv.index('--env')
        if pos_env + 1 >= len(sys.argv):
            print('错误：在-env命令行中没有指定运行环境！')
            sys.exit()

        run_setting = sys.argv[pos_env+1]
        del run_setting[pos_env+1]
        del run_setting[pos_env]
    else:
        run_setting = 'esc' if sys.platform == 'linux' else 'localhost'
    print('提示：命令行指定运行环境为', run_setting)

    setting_module = import_module('setting.%s' % run_setting)
    for k in dir(setting_module):
        if k.startswith('__'):
            continue
        v = getattr(setting_module, k)
        if not isinstance(v, types.ModuleType):
            setattr(settings, k, v)

    from django.core.management import execute_from_command_line



    execute_from_command_line(sys.argv)
