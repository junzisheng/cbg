from __future__ import absolute_import
from celery import Celery
app = Celery('service', include=['crawl_celery.tasks'])
app.config_from_object('crawl_celery.celeryconfig')


if __name__ == '__main__':
    app.start()