from django.contrib import admin
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.urls import reverse
from .calendar import EventCalendar
import datetime, calendar
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
    # list_display = ('id', 'day', 'timeofday', 'employee')
    # inlines = [SchedulerRecurringPatternInLine]
    list_display = ('day', 'timeofday', 'descripction')
    change_list_template = 'admin/calendars/calendar.html'

    def changelist_view(self, request, extra_context=None):
        after_day = request.GET.get('day__gte', None)
        extra_context = extra_context or {}
 
        if not after_day:
            d = datetime.date.today()
        else:
            try:
                split_after_day = after_day.split('-')
                d = datetime.date(year=int(split_after_day[0]), month=int(split_after_day[1]), day=1)
            except:
                d = datetime.datetime.today()
        print(d)
 
        previous_month = datetime.date(year=d.year, month=d.month, day=1)  # find first day of current month
        previous_month = previous_month - datetime.timedelta(days=1)  # backs up a single day
        previous_month = datetime.date(year=previous_month.year, month=previous_month.month,
                                       day=1)  # find first day of previous month
        
        last_day = calendar.monthrange(d.year, d.month)
        next_month = datetime.date(year=d.year, month=d.month, day=last_day[1])  # find last day of current month
        next_month = next_month + datetime.timedelta(days=1)  # forward a single day
        next_month = datetime.date(year=next_month.year, month=next_month.month,
                                   day=1)  # find first day of next month
 
        extra_context['previous_month'] = reverse('admin:schedules_scheduler_changelist') + '?day__gte=' + str(
            previous_month)
        extra_context['next_month'] = reverse('admin:schedules_scheduler_changelist') + '?day__gte=' + str(next_month)
        extra_context['add_schedule'] = reverse('admin:schedules_scheduler_add')

        cal = EventCalendar(firstweekday=0)
        html_calendar = cal.formatmonth(d.year, d.month, withyear=True)
        html_calendar = html_calendar.replace('<td ', '<td  width="150" height="150"')
        #print(mark_safe(html_calendar))
        extra_context['calendar'] = mark_safe(html_calendar)

        return super().changelist_view(request, extra_context)


@admin.register(SchedulerException)
class SchedulerExceptionnAdmin(admin.ModelAdmin):
    pass


@admin.register(SchedulerRecurringPattern)
class SchedulerRecurringPatternAdmin(admin.ModelAdmin):
    pass


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    pass


# @admin.register(SchedulerDay)
# class SchedulerDayAdmin(CalendarActionMixin, admin.ModelAdmin):
#     date_hierarchy = 'created'
#     change_list_template = 'admin/schedules/scheduler_day.html'
#     #form = SchedDayForm


# @admin.register(SchedulerMonth)
# class SchedulerMonthAdmin(admin.ModelAdmin):
#     change_list_template = 'admin/schedules/scheduler_month.html'


