from schedules.models import Activity
from users.models import CustomUser


def filter_transitions(file_reader):
    """
    filtra toda la serie de datos y solo se queda 
    con los primeros valores antes de cada transición
    es decir los primeros valores introducidos en el sistema
    de registro
    """
    temp_val = None
    for row in file_reader:
        if temp_val != row[4]:
            temp_val = row[4]
            yield ((row[0], row[3], row[4]))

def create_activity(ac, datetime, state):
    user = CustomUser.objects.get(number_employee=ac)
    # TODO
    print(ac, datetime, state)
    # Activity.objects.create(user, False, False, payment, start_work, end_work)