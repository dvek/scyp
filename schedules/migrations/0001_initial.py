# Generated by Django 2.0.5 on 2018-05-18 05:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('updated', models.DateTimeField(editable=False)),
                ('start_work', models.DateTimeField(blank=True, verbose_name='Hora de llegada')),
                ('end_work', models.DateTimeField(blank=True, verbose_name='Hora de salida')),
                ('is_holiday', models.BooleanField(verbose_name='Feriado')),
                ('is_weekend', models.BooleanField(verbose_name='Fin de semana')),
                ('payment', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Pago')),
                ('employee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Empleado')),
            ],
            options={
                'verbose_name': 'Actividad',
                'verbose_name_plural': 'Actividades',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('updated', models.DateTimeField(editable=False)),
                ('event_title', models.CharField(max_length=50, verbose_name='Titulo evento')),
                ('event_description', models.TextField(max_length=500, verbose_name='Descripcion evento')),
                ('start_datetime', models.DateTimeField(verbose_name='Fecha/Hora inicio')),
                ('end_datetime', models.DateTimeField(verbose_name='Fecha/Hora termino')),
                ('is_recurring', models.BooleanField(default=True, verbose_name='es recurrente')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
                ('parent_event', models.ForeignKey(blank=True, null=True, on_delete=None, to='schedules.Event', verbose_name='Evento padre')),
            ],
            options={
                'verbose_name': 'Evento',
                'verbose_name_plural': 'Eventos',
            },
        ),
        migrations.CreateModel(
            name='EventException',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('updated', models.DateTimeField(editable=False)),
                ('is_rescheduled', models.BooleanField(verbose_name='Es programado')),
                ('is_cancelled', models.BooleanField(verbose_name='Es cancelado')),
                ('start_datetime', models.DateTimeField(verbose_name='Fecha/Hora inicio')),
                ('end_datetime', models.DateTimeField(verbose_name='Fecha/Hora termino')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
                ('event', models.ForeignKey(on_delete=None, to='schedules.Event', verbose_name='Evento')),
            ],
            options={
                'verbose_name': 'Ocurrencia evento',
                'verbose_name_plural': 'Ocurrencias eventos',
            },
        ),
        migrations.CreateModel(
            name='RecurringPattern',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(editable=False)),
                ('updated', models.DateTimeField(editable=False)),
                ('title', models.CharField(max_length=50, verbose_name='Titulo')),
                ('separation_count', models.PositiveIntegerField(default=0, verbose_name='Conteo separacion')),
                ('max_num_occurrences', models.PositiveIntegerField(default=0, verbose_name='Max. num. ocurrencias')),
                ('day_of_week', models.PositiveSmallIntegerField(default=0, verbose_name='Dia de la semana')),
                ('week_of_month', models.PositiveSmallIntegerField(default=0, verbose_name='Semana del mes')),
                ('day_of_month', models.PositiveSmallIntegerField(default=0, verbose_name='Dia del mes')),
                ('month_of_year', models.PositiveSmallIntegerField(default=0, verbose_name='Mes del an~o')),
                ('event', models.ForeignKey(on_delete=None, to='schedules.Event', verbose_name='Evento')),
            ],
            options={
                'verbose_name': 'Patron recurrente',
                'verbose_name_plural': 'Patrones recurrentes',
            },
        ),
    ]
