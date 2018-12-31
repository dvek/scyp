from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from mptt.admin import MPTTModelAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import (
    CustomUser,
    Section,
    PaymentScale,
    Position,
    Increment)
from .utils import get_full_url
from core.middleware import get_current_request
from .mixins import UserAdminMixin

@admin.register(CustomUser)
class CustomUserAdmin(UserAdminMixin, UserAdmin):
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')
        }),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'document', 
            'birthdate', 'employment_date', 'address', 'phone', 
            'picture', 'type_employee', 'number_employee', 'section', 'position')
        })
    )

    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password')
        }),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'document', 
            'birthdate', 'employment_date', 'address', 'phone', 
            'picture', 'type_employee', 'number_employee', 'section', 'position')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser',
            'groups', 'user_permissions')
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined')
        })
    )

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'first_name', 'last_name', 'document', 'type_employee', 'image_tag']

    def image_tag(self, obj):
        request = get_current_request()
        return mark_safe('<img src="{}" height="{}"/>'.format(
            get_full_url(obj.picture, request),
            '50px'
        ))
    image_tag.short_description = 'Fotografia'
    

@admin.register(Section)
class SectionAdmin(MPTTModelAdmin):
    #list_display = ('id', )
    mptt_level_indent = 20


@admin.register(PaymentScale)
class PaymentScaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'position', 'amount')


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'position_name')


@admin.register(Increment)
class IncrementAdmin(admin.ModelAdmin):
    list_display = ('id', 'percentage', 'created')