from django.contrib import admin, messages

from .models import RegisterUploaded
from .exceptions import TrackingActivityException
from .forms import RegisterUploadedForm


def reset_state(modeladmin, request, queryset):
    queryset.update(status='created')
    messages.add_message(request, messages.INFO, 'Tareas de registros canceladas')
reset_state.short_description = 'Seleccione los registros para cancelar'


@admin.register(RegisterUploaded)
class RegisterUploadedAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'status', 'result')
    readonly_fields = ('status', 'result')
    actions = [reset_state]
    forms = [RegisterUploadedForm]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

    def response_change(self, request, obj):
        if '_process' in request.POST:
            obj.save()
            obj.processing_data()
            self.message_user(request, 'Procesando archivo', level=messages.INFO)
        return super().response_change(request, obj)


    
