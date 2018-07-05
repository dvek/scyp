from django import forms
from django.core.exceptions import ValidationError


class SchedDayForm(forms.ModelForm):
    day_date = forms.DateField(help_text='Seleccione un día')
