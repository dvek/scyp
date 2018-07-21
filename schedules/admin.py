from django.contrib import admin
from django.utils import timezone


from .models import (
    TimeOfDay,
    Scheduler,
    SchedulerException,
    SchedulerRecurringPattern,
    Activity,
    SchedulerDay,
    SchedulerMonth)
from .forms import SchedDayForm
from .mixins import AdminCommonMixin, CalendarActionMixin

class SchedulerRecurringPatternInLine(admin.StackedInline):
    model = SchedulerRecurringPattern
    extra = 1


@admin.register(TimeOfDay)
class TimeOfDayAdmin(admin.ModelAdmin):
    pass


@admin.register(Scheduler)
class SchedulerAdmin(AdminCommonMixin, admin.ModelAdmin):
    list_display = ('id', 'day', 'timeofday', 'employee')
    # inlines = [SchedulerRecurringPatternInLine]


@admin.register(SchedulerException)
class SchedulerExceptionnAdmin(admin.ModelAdmin):
    pass


@admin.register(SchedulerRecurringPattern)
class SchedulerRecurringPatternAdmin(admin.ModelAdmin):
    pass


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    pass


@admin.register(SchedulerDay)
class SchedulerDayAdmin(CalendarActionMixin, admin.ModelAdmin):
    date_hierarchy = 'created'
    change_list_template = 'admin/schedules/scheduler_day.html'
    #form = SchedDayForm

    


@admin.register(SchedulerMonth)
class SchedulerMonthAdmin(admin.ModelAdmin):
    change_list_template = 'admin/schedules/scheduler_month.html'