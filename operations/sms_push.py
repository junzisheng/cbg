__author__ = 'gwj'

import uuid
import json
import os
import sys
import time
from operations.functions import get_cbg_path
from operations.thread_manager import WorkManager, Work
sys.path.insert(0, get_cbg_path())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cbg_backup.settings")
import django
from cbg_backup import settings
settings.LOGGING_CONFIG = False
django.setup()
from user.models import AliSmsQueue
from libraries.ali_sms import sms_send
from libraries.cbg_logging import get_logger

logger = get_logger('sms_log')



# class DelSms(threading.Thread):
#     """删除已发短信的"""
#     __GET_NUM = 1000
#
#     def __init__(self):
#         """
#         :param queue        : token 队列
#         """
#         threading.Thread.__init__(self)
#
#     def run(self):
#         """主线程函数，每次从队列中取GET_NUM条进行推送执行"""
#         while True:
#             try:
#                 data_fetch = []
#                 while not sms_del_queue.empty():
#                     data_fetch.append(sms_del_queue.get())
#                     if len(data_fetch) >= self.__GET_NUM:
#                         break
#
#                 if data_fetch:
#                     AliSmsQueue.objects.filter(id__in=data_fetch).delete()
#                     transaction.commit()
#                     data_fetch = []
#             except Exception as e:
#                 print(e)
#             time.sleep(3)


def ali_sms_send(sms_dict):
    """发送阿里短信"""
    # debug模式下不发送短信
    if settings.DEBUG is True:
        logger.info('短信发送...类型:【%s】 【%s】>>>【%s】' % (sms_dict['type'] ,sms_dict['umobile'], sms_dict['params']))
        return
    if time.time() > sms_dict['deadline']:
        logger.info('短信已经过期【%s】已经过期，不再发送' % (sms_dict['params']))
        return
    params = sms_dict['params']
    result = sms_send.send_sms(uuid.uuid1(), sms_dict['umobile'], sms_dict['sign_name'], sms_dict['template_code'], params)
    result = json.loads(result.decode())
    # 错误的话打印日志
    if result['Code'] != 'OK':
        logger.warning('发送短信(%s)【%s】到【%s】失败, 错误信息:%s  %s' %
                       (sms_dict['type'], sms_dict['params'], sms_dict['umobile'], result['Code'], result['Message']))
    else:
        logger.info('短信发送成功...类型:【%s】 【%s】>>>【%s】' % (sms_dict['type'] ,sms_dict['umobile'], sms_dict['params']))

if __name__ == '__main__':
    p = settings.redis3.pubsub()
    p.subscribe(['sms_notify'])
    # 开启工作线程
    work_manager = WorkManager()
    # 开启删除短信的线程
    # DelSms().start()

    for item in p.listen():
        if item['type'] == 'message':
            sms_list = json.loads(item['data'].decode())
            if item['channel'] == b'sms_notify':
                for sms_dict in sms_list:
                    print(sms_dict)
                    work_manager.get_queue().put((ali_sms_send, sms_dict))

