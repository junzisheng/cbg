#encoding=utf-8
from __future__ import absolute_import
import sys
import os
import multiprocessing
# 初始化django环境
# from core.functions import get_cbg_path
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cbg_backup.settings")
# sys.path.insert(0, get_cbg_path())
from crawl_celery.celery_init import app
# import django
# django.setup()

if 'time' in sys.modules.keys():
    del sys.modules['time']

"""
由于在celery中gevent使用的是monkey.patch_all()  将threading打了补丁变为协程  且在上面将time解除了补丁， 因此在threading中time.sleep(会导致整个进程堵塞)
"""
# if 'threading' in sys.modules.keys():
#     del sys.modules['threading']
from celery import Task
from .crawl.Base_Class import TaskManager, Logger
from .crawl import crawl_class


class MyTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        # print('task done: {0}'.format(retval)
        return super(MyTask, self).on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # print 'task fail, reason: {0}'.format(exc)
        return super(MyTask, self).on_failure(exc, task_id, args, kwargs, einfo)


@app.task(bind=True, base=MyTask)
def crawl_task(self, *args, **kwargs):
    """
    完成爬取的工作
    """
    # 重新导入模块， 为了以后在不关闭celery的前提下更新crawl_class模块从而生效
    #importlib.reload(crawl_class)
    # try:
    try:
        crawl_obj = TaskManager.init_crawl_obj(*args, **kwargs)
        crawl_obj.run()
    except:
        Logger.cls_error.exception('tasks错误')
    # except Exception as e:
    #     TaskManager.Logger.cls_error.exception('错误')
    #     raise self.retry(exc=e, countdown=5, max_retries=3)

if __name__ == 'crawl_celery.tasks':
    if 'worker' in sys.argv:
        from multiprocessing import Queue
        crawl_class.Base_Crawl.task_manager = TaskManager
        TaskManager.init(1, crawl_class.BBCrawl)  # 1：召唤兽
        TaskManager.init(2, crawl_class.RoleCrawl) # 2 : 角色
        TaskManager.init(3, crawl_class.EquipCrawl)  # 3: 装备
        # 开启插入数据库的进程
        queue = multiprocessing.Queue(maxsize=500)
        TaskManager.queue = queue
        p = multiprocessing.Process(target=TaskManager.do_sql, args=(queue, TaskManager.crawl_cls_list))
        p.start()


