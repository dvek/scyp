from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from datetime import datetime, date, time
import pytz
from core.models import TrackerModel
from .managers import SchedulerManager

class TimeOfDay(TrackerModel):
    """
    represent a fraction of day like
    mornig, evening, night, or custom
    """
    name = models.CharField(max_length=150)
    start_time = models.TimeField(verbose_name='Hora inicio', null=True)
    end_time = models.TimeField(verbose_name='Hora termino', null=True)

    class Meta:
        verbose_name = 'Etapa'
        verbose_name_plural = 'Etapas'

    def __str__(self, *args, **kwargs):
        return self.name

        
class SchedulerBase(TrackerModel):
    """
    base model that represent a calendar scheduled
    with info from fraction day + specific day
    """
    day = models.DateField(null=True, verbose_name='Dia')
    timeofday = models.ForeignKey(TimeOfDay, null=True, on_delete=models.SET_NULL, verbose_name="Periodo")

    class Meta:
        abstract = True


class Scheduler(SchedulerBase):
    """
    represent a employee time interval for certain day, that user can work in this range
    this interval for work may be recurrrent with a certain pattern
    """
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, verbose_name='Empleado')
    is_recurring = models.BooleanField(default=True, verbose_name="Es recurrente")
    descripction = models.TextField(null=True, verbose_name='Descripción', blank=True)
    parent_event = models.ForeignKey('self', null=True, blank=True, on_delete=None, verbose_name='Planificado origen')

    objects = SchedulerManager()
    class Meta:
        verbose_name = 'Calendaio'
        verbose_name_plural = 'Calendarios'

    def __str__(self):
        return '<Panificador: empleado: {}, Etapa: {}>'.format(
            self.employee,
            self.timeofday)
    
    def get_absolute_url(self):
        url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.id])
        return '<a href="%s">%s - %s</a>' % (
            url,
            str(self.timeofday),
            self.employee)



class SchedulerRecurringPattern(TrackerModel):
    """
    represent the patterns for cases when scheduled event are recurring
    ej: 2 times for week, every day, every month, etc.
    """
    scheduler = models.ForeignKey(Scheduler, null=True, on_delete=models.SET_NULL, verbose_name='Planificador')
    title = models.CharField(max_length=50, verbose_name='Título')
    separation_count = models.PositiveIntegerField(default=0, verbose_name='Conteo separación')
    max_num_occurrences = models.PositiveIntegerField(default=0, verbose_name='Max. num. ocurrencias')
    day_of_week = models.PositiveSmallIntegerField(default=0, verbose_name='Día de la semana')
    week_of_month = models.PositiveSmallIntegerField(default=0, verbose_name='Semana del mes')
    day_of_month = models.PositiveSmallIntegerField(default=0, verbose_name='Día del mes')
    month_of_year =  models.PositiveSmallIntegerField(default=0, verbose_name='Mes del año')

    class Meta:
        verbose_name = "Patron recurrente"
        verbose_name_plural = "Patrones recurrentes"

    def __str__(self):
        return '{} description: {}'.format(
            self.scheduler,
            self.title)


class SchedulerException(TrackerModel):
    scheduler = models.ForeignKey(Scheduler, null=True, on_delete=models.SET_NULL, verbose_name='Planificador')
    is_rescheduled = models.BooleanField(verbose_name='Es reprogramado')
    is_cancelled = models.BooleanField(verbose_name='Es cancelado')
    start_datetime = models.DateTimeField(verbose_name='Fecha/Hora inicio')
    end_datetime = models.DateTimeField(verbose_name='Fecha/Hora termino')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        null=True,
        blank=True, 
        on_delete=models.SET_NULL,
        verbose_name='Creado por')

    class Meta:
        verbose_name = "Ocurrencia planificador"
        verbose_name_plural = "Ocurrencias planificador"


class Activity(SchedulerBase):
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name='activity_employee',
        verbose_name='Empleado')
    is_holiday = models.BooleanField(verbose_name='Feriado')
    is_weekend = models.BooleanField(verbose_name='Fin de semana')
    payment = models.DecimalField(verbose_name='Pago', max_digits=6, decimal_places=2)

    class Meta:
        verbose_name = "Actividad"
        verbose_name_plural = "Actividades"

    def __str__(self):
        return "<Horario: {} de: {} hasta: {}>".format(
            self.employee,
            self.start_work,
            self.end_work)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # process_payments(self)


class SchedulerMonth(Scheduler):
    class Meta:
        proxy = True
        verbose_name = 'Calendario Mes'


class SchedulerDay(Scheduler):

    class Meta:
        proxy = True
        verbose_name = 'Calendario Día'

