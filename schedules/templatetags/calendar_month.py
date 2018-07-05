from django import template
from django.utils import timezone

from schedules.services import get_times_from_day
from schedules.models import TimeOfDay

register = template.Library()


@register.inclusion_tag('templatetags/calendar_month.html')
def calendar_month():
    variable = None
    print(">>>>>>")
    return {'variable': variable}
