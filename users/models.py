from django.contrib.auth.models import AbstractUser
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from core.models import TrackerModel
from .services import update_payments
from .managers import PaymentScaleManager


def get_path_files(instance, filename):
    return '{}/{}'.format(
        instance.username,
        filename
    )


class Section(MPTTModel):
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre seccion')
    parent = TreeForeignKey(
        'self', null=True, blank=True, related_name='children', db_index=True, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Seccion'
        verbose_name_plural = 'Secciones'

    def __str__(self):
        cantidad = self.cantidad_func()
        return '{} ({} {})'.format(
            self.name, 
            cantidad,
            'funcionarios' if cantidad > 1 else 'funcionario')

    def cantidad_func(self):
        return self.employees.count()


class Position(TrackerModel):
    position_name = models.CharField(max_length=30, verbose_name='Nombre del cargo')

    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'

    def __str__(self):
        return self.position_name


class PaymentScale(TrackerModel):
    position = models.OneToOneField(
        Position,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Cargo')
    amount = models.DecimalField(
        max_digits=12, 
        decimal_places=4,
        help_text='Para decimales use ",". Hasta 4 decimales')

    object = PaymentScaleManager()

    class Meta:
        verbose_name = 'Nivel de pago'
        verbose_name_plural = 'Niveles de pago'

    def __str__(self):
        return '{}: ${}'.format(self.position, self.amount)


class Increment(TrackerModel):
    percentage = models.IntegerField(verbose_name='Porcentaje de incremento %')

    class Meta:
        verbose_name = 'Incremento'
        verbose_name_plural = 'Incrementos'

    def __str__(self):
        return str(self.percentage)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        update_payments(PaymentScale.objects.all(), self.percentage/100)



class CustomUser(AbstractUser):
    GENDER_CHOICES = (('M', 'Masculino'), ('F', 'Femenino'))
    TYPE_EMPLOYEE_CHOICES = (('A', 'Administrativo'),('T', 'Tecnico'))

    document = models.CharField(max_length=15, null=True, blank=True, verbose_name='Documento identidad')
    birthdate = models.DateField(null=True, blank=True, verbose_name='Fecha nacimiento')
    employment_date = models.DateField(null=True, blank=True, verbose_name='Fecha de empleo')
    address = models.TextField(null=True, blank=True, verbose_name='Direccion')
    phone = models.CharField(max_length=150, null=True, blank=True,  verbose_name='Teléfono/Celular')
    picture = models.ImageField(upload_to=get_path_files, null=True, blank=True, verbose_name='Fotografía')
    type_employee = models.CharField(max_length=1, choices=TYPE_EMPLOYEE_CHOICES, 
        verbose_name='Tipo empleado', null=True, blank=True)
    number_employee = models.CharField(max_length=15, verbose_name='AC No.', null=True)
    section = models.ForeignKey('users.Section', null=True, blank=True, 
        verbose_name='Sección', on_delete=models.SET_NULL, related_name='employees')
    position = models.ForeignKey(Position, null=True, 
        on_delete=models.SET_NULL, verbose_name='Cargo')

    
    def __str__(self):
        if self.first_name is None and self.last_name is None:
            return self.email
        return '{} {}'.format(self.first_name, self.last_name)



