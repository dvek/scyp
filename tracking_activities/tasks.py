from __future__ import absolute_import, unicode_literals
import time, csv, os
from celery import shared_task
from django.core.exceptions import ValidationError
from django.db import transaction
from django.apps import apps
from django.conf import settings

from .exceptions import TrackingActivityException
from .services import (
    filter_transitions,
    create_activity)


@shared_task
def import_data(obj_id):
    model =  apps.get_model('tracking_activities.RegisterUploaded')
    try:
        obj = model.objects.get(id=obj_id)
        with transaction.atomic():
            processor_csv(
                obj.file,
                settings.CSV_DELIMITER,
                settings.CSV_MARK_START,
                settings.CSV_MARK_END)
    except TrackingActivityException as ex:
        obj.status = model.ERROR
        obj.result = str(ex)
        obj.save()
    else:
        obj.status = model.SUCCESS
        obj.result = None
        obj.save()


def processor_csv(file, delimiter, mark_start, mark_end):
    try:
        with open(file.path, 'r') as csvfile:
            file_reader = csv.reader(csvfile, delimiter=delimiter)
            next(file_reader, None)
            gen_filtered = filter_transitions(file_reader)
            for ac, dt, state in gen_filtered:
                create_activity(ac, dt, state)
    except (csv.Error, Exception) as ex:
        raise TrackingActivityException('Error al procesar el archivo CSV: %s' % str(ex) )

