from __future__ import absolute_import
import types

from django.contrib.staticfiles.storage import staticfiles_storage
try:
    from django.core.urlresolvers import reverse
except:
    from django.urls import reverse

from jinja2 import Environment

from cbg_backup import filters

# class Environment_(Environment):
#     __instance = None
#     def __init__(self, *args, **kwargs):
#         super(Environment, self).__init__(**kwargs)
#
#     def __new__(cls, *args, **kwargs):
#         if not



def environment(**options):
    if not environment.env:
        env = Environment(**options)
        env.globals.update({
            'static': staticfiles_storage.url,
            'url': reverse,
        })
        for k in dir(filters):
            v = getattr(filters, k)
            if k not in ['contextfilter'] and not k.startswith('_') and isinstance(v, types.FunctionType):
                if k in env.filters:
                    print('警告：过滤器%s已经在%s中定义了' % (k, k.__module__))
                env.filters[k] = v
        environment.env = env
    return environment.env


environment.env = None