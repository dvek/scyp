import asyncio, time
from concurrent.futures import ThreadPoolExecutor
from django.db import models
from django.core.exceptions import ValidationError

from core.models import TrackerModel
from .services import import_data
from .exceptions import TrackingActivityException


class RegisterUploaded(TrackerModel):

    CREATED = 'created'
    PROCESSING = 'processing'
    SUCCESS = 'success'
    ERROR = 'error'
    CANCELED = 'canceled'

    STATUS_CHOICES = (
        (CREATED, 'Creado'),
        (PROCESSING, 'Procesando'),
        (SUCCESS, 'Finalizado'),
        (ERROR, 'Error'),
        (CANCELED, 'Cancelado')
    )

    file = models.FileField(upload_to='uploads/registers/%Y/%m/%d/', verbose_name='Archivo')
    status = models.CharField(max_length=15, default=CREATED, choices=STATUS_CHOICES, verbose_name='Estado')
    result = models.TextField(null=True, verbose_name='Resultado')
    
    class Meta:
        verbose_name = "Registro subido"
        verbose_name_plural = "Registros subidos"

    def __str__(self):
        return 'Archivo: %s' % self.file.name.split('/')[-1]

    def clean(self):
        if self.status == RegisterUploaded.PROCESSING:
            raise ValidationError('Actualmente ya se esta procesando el archivo')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def processing_data(self, *args, **kwargs):
        # async operation, slow operation
        pool = ThreadPoolExecutor(2)
        loop = asyncio.new_event_loop()
        loop.run_in_executor(pool, import_data, self.id)
