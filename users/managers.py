from django.db import models
from django.contrib.auth.models import BaseUserManager


class PaymentScaleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-amount')


class UserQuerySet(models.QuerySet):
    
    def users_by_section(self, sections):
        return self.filter(section__in=sections)


class UserManager(BaseUserManager):

    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)

    def users_by_section(self, sections):
        return self.get_queryset().users_by_section(sections=sections)