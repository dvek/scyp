from django.db import models


class SchedulerQuerySet(models.QuerySet):
    
    def timesofdays(self):
        return self.filter(timeofday__isnull=False).order_by('created')

    def user_by_sections(self, user):
        if user is None:
            return self
        users = []
        descendants = user.section.get_descendants(include_self=True)
        for desc in descendants:
            users = users + list(desc.employees.all())
        print(users)
        return self.filter(employee__in=users)

class SchedulerManager(models.Manager):
    def get_queryset(self):
        return SchedulerQuerySet(self.model, using=self._db) 

    def timesofdays(self):
        return self.get_queryset().timesofdays()