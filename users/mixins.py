

class UserAdminMixin(object):
    """
    set helps methods for user admin
    """
    def get_queryset(self, request):
        """
        lee el queryset de todos los objectos si es superuser
        de otra forma solo lee los objectos que ha modificado o es propietario
        """
        qs = self.model.objects.get_queryset()
        if request.user.is_superuser:
            return qs
        return qs.users_by_section(request.user.get_child_sections())

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_by', None) is None:
            obj.created_by = request.user
        obj.save()
