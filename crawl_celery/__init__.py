import os, sys
if 'worker' in sys.argv:  # celery开启需要初始化django模型
# if True:
    from core.functions import get_cbg_path
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cbg_backup.settings")
    sys.path.insert(0, get_cbg_path())
    import django
    django.setup()
