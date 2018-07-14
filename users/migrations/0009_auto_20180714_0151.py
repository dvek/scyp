# Generated by Django 2.0.4 on 2018-07-14 05:51

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20180617_1744'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='paymentscale',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='increment',
            name='created',
            field=models.DateTimeField(editable=False, verbose_name='Creado'),
        ),
        migrations.AlterField(
            model_name='increment',
            name='percentage',
            field=models.IntegerField(verbose_name='Porcentaje de incremento %'),
        ),
        migrations.AlterField(
            model_name='increment',
            name='updated',
            field=models.DateTimeField(editable=False, verbose_name='Modificado'),
        ),
        migrations.AlterField(
            model_name='paymentscale',
            name='amount',
            field=models.DecimalField(decimal_places=4, help_text='Para decimales use ",". Hasta 4 decimales', max_digits=12),
        ),
        migrations.AlterField(
            model_name='paymentscale',
            name='created',
            field=models.DateTimeField(editable=False, verbose_name='Creado'),
        ),
        migrations.AlterField(
            model_name='paymentscale',
            name='updated',
            field=models.DateTimeField(editable=False, verbose_name='Modificado'),
        ),
        migrations.AlterField(
            model_name='position',
            name='created',
            field=models.DateTimeField(editable=False, verbose_name='Creado'),
        ),
        migrations.AlterField(
            model_name='position',
            name='updated',
            field=models.DateTimeField(editable=False, verbose_name='Modificado'),
        ),
    ]