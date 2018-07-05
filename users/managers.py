from django.db import models


class PaymentScaleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-amount')