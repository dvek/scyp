# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


class TrackerModel(models.Model):
    """
    Abstract class model with fields modificado and modificado
    for tracking purpouses
    """
    created = models.DateTimeField(editable=False, verbose_name='Creado')
    updated = models.DateTimeField(editable=False, verbose_name='Modificado')

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            if self.created is None:
                self.created = timezone.now()
        self.updated = timezone.now()
        super(TrackerModel, self).save(*args, **kwargs)
