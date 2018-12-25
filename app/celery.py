from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# settings celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')
app.config_from_object('django.conf:settings', namespace='CELERY')

# load task modules from all apps
app.autodiscover_tasks()