from django import template
from django.utils import timezone

from schedules.services import get_all_times

register = template.Library()

@register.inclusion_tag('templatetags/calendar_day.html')
def calendar_day(event_lists):
    # times_of_day = TimeOfDay.objects.all()
    # year, month, day = timezone.now().year, timezone.now().month, timezone.now().day
    return {
        'results': event_lists,
        'tod_list': get_all_times(),
    }