from .models import TimeOfDay


def get_times_from_day(year, month, day, times):
    return times

def get_all_times():
    return TimeOfDay.objects.all().values('id', 'name')

def process_payments(activity):
    """
    find all occurrences with schedultes model
    and if existe then save payment in this activity record
    """
    pass