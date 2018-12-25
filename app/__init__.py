from __future__ import absolute_import, unicode_literals

# app is always imported whe start django app
from .celery import app as celery_app

__all__ = ('celery_app')