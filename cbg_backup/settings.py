import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '!%n_^8nvogk*&0up%4#f2+s2b&-4djt-wl=!6*l!4e9ysc55zj'

DEBUG = False
DEBUG_CURSOR = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djcelery',
    'core',
    'crawl_celery',
    'service',
    'others',
    'user',
    'order',
    'activity',
    'coupon',
    'middleware',
    'xadmin',
    'crispy_forms'
    # 'reversion',
)


MIDDLEWARE = [
    'middleware.webrequestmonitor.WebRequestMonitor',  # 监测性能
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.transaction.TransactionMiddleware',
    'middleware.gpub.PublicMiddleWare',  # 视图处理的前置处理
]

MIDDLEWARE_CLASSES = MIDDLEWARE

ROOT_URLCONF = 'cbg_backup.urls'

# 配置jinja模板
CONTEXT_PROCESSORS = [
    'django.template.context_processors.debug',
    'django.template.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': CONTEXT_PROCESSORS,
        },
    },
    {
        'BACKEND': 'cbg_backup.backends.Jinja2Backend',
        'DIRS': ['templates', ''],
        'APP_DIRS': True,
        'OPTIONS': {
            'environment': 'cbg_backup.jinja_env.environment',
            'context_processors': CONTEXT_PROCESSORS,
            #'extensions': [your extensions here],
        },
    },
]

WSGI_APPLICATION = 'cbg_backup.wsgi.application'

CACHES = {
    "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://:Xj3.14164@47.104.193.247:6379/5",
            "KEY_FUNCTION": "unit.cache.key_func",
            "KEY_PREFIX": "cache",
            'OPTIONS': {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
    },
}
# SESSION_COOKIE_AGE = -1 #设置session过期时间为30分钟
# '''配置session引擎SESSION_ENGINE为redis，配置此处session会存储在redis中，不会再去操作数据库了'''
# SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
# 使用redis保存session数据
SESSION_ENGINE = 'redis_sessions.session'
SESSION_REDIS_HOST = '127.0.0.1'
SESSION_REDIS_PORT = 6379
SESSION_REDIS_DB = 6
SESSION_REDIS_PASSWORD = 'Xj3.14164'
SESSION_REDIS_PREFIX = 'session'
# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

# DATABASES = {'default': {   'ENGINE'    :   'django.db.backends.mysql',
#                             'NAME'      :   'cbg',
#                              # 'NAME'      :   'sql_test',
#                              'USER'      :   'wordpress',
#                              'PASSWORD'  :   'Xj3.14164',
#                              'HOST'      :   '127.0.0.1',
#                              'PORT'      :   '3306',
#                          },
#               }


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'
#TIME_ZONE = 'UTC'

USE_I18N = False
#
USE_L10N = True

# USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
# if DEBUG is False:
#     STATIC_ROOT = 'static'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
UPLOAD_DIRS = os.path.join(STATICFILES_DIRS[0], 'upload')

# # 配置dcelery
# import djcelery
# djcelery.setup_loader()
# BROKER_URL = 'redis://:Xj3.14164@122.152.195.174:6379/1'
RENDER_BASE = {}  # 定义一些公共的模板
#DOMAIN = '' # 设置网站的doamin

AUTH_PROFILE_MODULE = 'user.UserProfile'
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # session在浏览器关闭失效


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(process)s:%(name)s:%(lineno)d] - %(message)s'
        },
        'simple': {
            'format': '%(asctime)s %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'cbg.debug.log',
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'paysapi': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'cbg.paysapi.log',
            'formatter': 'simple',
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'cbg.error.log',
            'formatter': 'standard',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['default', 'console', 'error'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['default', 'console', 'error'],
            'level': 'DEBUG',
            'propagate': False
        },
        'paysapi': {
            'handlers': ['paysapi'],
            'level': 'DEBUG',
            'propagate': False,
        }
    }
}

from share.functions import import_setting_by_name, path_insert
import_setting_by_name(sys.modules[__name__])
path_insert(BASE_DIR)


# 邮箱设置
EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.126.com'  # 如果是 163 改成 smtp.163.com
EMAIL_PORT = 465
EMAIL_HOST_USER = 'cbg_crawl@126.com' # 帐号
EMAIL_HOST_PASSWORD = 'g527910351'  # 密码
DEFAULT_FROM_EMAIL = '藏宝阁助手 <%s>' % EMAIL_HOST_USER

