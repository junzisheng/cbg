#encoding=utf-8
from __future__ import absolute_import
import sys
import datetime
from django.db import transaction

from order.models import CbgOrders, CbgOrderDetail
from user.models import CbgSysInfo
import multiprocessing
from crawl_celery.celery_init import app
from cbg_backup import settings

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
        # 任务完成后的操作
        # 1. 修改订单状态
        with transaction.atomic():
            try:
                now = datetime.datetime.now()
                order_info = args[2]
                order = CbgOrders.objects.get(id=order_info['order_id'])
                order.status = '已完成'
                order.closing_time = now
                order.save(pre_status='进行中')
                service = CbgOrderDetail.objects.get(order_id=order.id)
                service.closing_time = now
                service.save()
                CbgSysInfo.objects.create(user_id=order_info['user_id'], content="您的订单已经完成", href="/order/main?status=已完成",
                                          create_time=now, type="notic", display_time=now)
                settings.redis3.hincrby('user_message', '%s:%s' % ('notic', order_info['user_id']))
            except:
                Logger.cls_error.exception('任务完成时发生错误')
        # 2. 给用户通知
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


