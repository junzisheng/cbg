CELERY_IMPORTS = ("request.tasks")
BROKER_URL = 'redis://:Xj3.14164@122.152.195.174:6379/1'
CELERY_RESULT_BACKEND = 'redis://:Xj3.14164@122.152.195.174:6379/1'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24   # 任务过期时间
CELERY_ACCEPT_CONTENT = ["pickle", "json"]            # 指定任务接受的内容类型.
CELERY_TIMEZONE = 'Asia/Shanghai'
# 某个程序中出现的队列，在broker中不存在，则立刻创建它
CELERY_CREATE_MISSING_QUEUES = True
CELERYD_CONCURRENCY = 20  # 并发worker数
CELERYD_FORCE_EXECV = True    # 非常重要,有些情况下可以防止死锁
CELERYD_MAX_TASKS_PER_CHILD = 100
# CELERYD_TASK_TIME_LIMIT = 60    # 单个任务的运行时间不超过此值，否则会被SIGKILL 信号杀死
CELERY_DISABLE_RATE_LIMITS = True



