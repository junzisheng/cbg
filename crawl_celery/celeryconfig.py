import sys
if sys.platform != 'linux':
    BROKER_URL = 'redis://:Xj3.14164@127.0.0.1:6379/1'
else:
    BROKER_URL = 'redis://:Xj3.14164@47.104.193.247:6379/1'
CELERY_IMPORTS = ("service.tasks")
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24
CELERY_ACCEPT_CONTENT = ["json"]            # ָ��������ܵ���������.
CELERY_TIMEZONE = 'Asia/Shanghai'
# ĳ�������г��ֵĶ��У���broker�в����ڣ������̴�����
CELERY_CREATE_MISSING_QUEUES = True
CELERYD_CONCURRENCY = 20 # 并发数
CELERYD_FORCE_EXECV = True    #
CELERYD_MAX_TASKS_PER_CHILD = 50 # 每个并发完成多少个任务就销毁进程 跟并发数没关系
# CELERYD_TASK_TIME_LIMIT = 60    #
CELERY_DISABLE_RATE_LIMITS = True



