from __future__ import absolute_import
from celery import Celery
app = Celery('request', include=['request.tasks'])
app.config_from_object('request.celeryconfig')


if __name__ == '__main__':
    app.start()