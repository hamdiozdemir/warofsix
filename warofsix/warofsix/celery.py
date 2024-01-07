from __future__ import absolute_import, unicode_literals
import os
from decouple import config

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'warofsix.settings')


app = Celery('warofsix', broker='amqp://localhost:5672')

app.config_from_object('django.conf:settings', namespace="CELERY")

app.autodiscover_tasks()

CELERY_BROKER_URL='amqp://rabbitmq:5672'
