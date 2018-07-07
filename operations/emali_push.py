import sys
import os
import time
from operations.functions import get_cbg_path
from operations.thread_manager import Work, WorkManager
sys.path.insert(0, get_cbg_path())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cbg_backup.settings")
import django
from cbg_backup import settings
from django.core.mail import send_mail
settings.LOGGING_CONFIG = False
django.setup()


if __name__ == '__main__':
    p = settings.redis3.pubsub()
    p.subscribe(['email_notify'])
    # work_manager = WorkManager()
    # for i in range(100):
    r = send_mail('【藏宝阁助手通知】', '您设置的商品有新的上架：http://niao2233.com?%s ' % time.time(),
                  settings.DEFAULT_FROM_EMAIL, ['1298477514@qq.com', 'guwenjiang@namibox.com'], fail_silently=False)
    print(r)
    #     time.sleep(1)
    #     print(r)

