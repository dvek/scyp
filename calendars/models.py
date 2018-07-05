from django.db import models
from django.conf import settings

from core.models import TrackerModel


class Day(TrackerModel):
    date = models.DateField(verbose_name='Dia')
    is_holiday = models.BooleanField(default=False, verbose_name='Es feriado')
    is_weekend = models.BooleanField(default=False, verbose_name='Es fin de semana')
    
    
    class Meta:
        verbose_name = "Dia"
        verbose_name_plural = "Dias"

