from django.db import models


class SchedulerQuerySet(models.QuerySet):
    
    def timesofdays(self):
        return self.filter(timeofday__isnull=False).order_by('created')

class SchedulerManager(models.Manager):
    def get_queryset(self):
        return SchedulerQuerySet(self.model, using=self._db) 

    def timesofdays(self):
        return self.get_queryset().timesofdays()