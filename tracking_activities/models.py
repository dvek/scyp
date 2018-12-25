import time, logging
from concurrent.futures import ThreadPoolExecutor
from django.db import models
from django.core.exceptions import ValidationError

from core.models import TrackerModel
from .exceptions import TrackingActivityException
from .tasks import import_data


logger = logging.getLogger(__name__)


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
        logger.info('Guardando registro subido...')
        super().save(*args, **kwargs)

    def processing_data(self, *args, **kwargs):
        # slow operation
        self.status = self.PROCESSING
        self.save()
        import_data.delay(self.id)
