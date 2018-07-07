import sys
import types
from share.setting_share import setting_name
from importlib import import_module


def import_setting_by_name(settings_module_import):
    """根据名字将指定name的配置文件导入本名字空间"""
    try:
        module_setting = import_module('setting.' + setting_name)
    except ImportError:
        print('错误：setting目录下不存在名为%s的配置环境!' % setting_name)
        sys.exit()
    for k in dir(module_setting):
        v = getattr(module_setting, k)
        if k.startswith('__'):
            continue
        elif not isinstance(v, types.ModuleType):
            setattr(settings_module_import, k, v)