from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class RegisterUploadedForm(forms.ModelForm):
    pass