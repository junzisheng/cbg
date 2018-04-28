import sys
if sys.platform == 'linux':
    BROKER_URL = 'redis://:Xj3.14164@127.0.0.1:6379/1'
else:
    BROKER_URL = 'redis://:47.104.193.247:6379/1'
CELERY_IMPORTS = ("request.tasks")
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24   # �������ʱ��
CELERY_ACCEPT_CONTENT = ["pickle", "json"]            # ָ��������ܵ���������.
CELERY_TIMEZONE = 'Asia/Shanghai'
# ĳ�������г��ֵĶ��У���broker�в����ڣ������̴�����
CELERY_CREATE_MISSING_QUEUES = True
CELERYD_CONCURRENCY = 20  # ����worker��
CELERYD_FORCE_EXECV = True    # �ǳ���Ҫ,��Щ����¿��Է�ֹ����
CELERYD_MAX_TASKS_PER_CHILD = 100
# CELERYD_TASK_TIME_LIMIT = 60    # �������������ʱ�䲻������ֵ������ᱻSIGKILL �ź�ɱ��
CELERY_DISABLE_RATE_LIMITS = True



