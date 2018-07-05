from .models import TimeOfDay


def get_times_from_day(year, month, day, times):
    return times

def get_all_times():
    return TimeOfDay.objects.all().values('id', 'name')

def calculate_payment(schedule)