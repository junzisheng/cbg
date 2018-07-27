import os, sys
if 'worker' in sys.argv or 'flower' in sys.argv:  # celery开启需要初始化django模型
# if True:
    from cbg_backup import settings
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cbg_backup.settings")
    delattr(settings, 'LOGGING')
    import django
    django.setup()

