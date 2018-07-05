import threading
from django.utils.deprecation import MiddlewareMixin

_thread_local = threading.local()


class RequestMiddleware(MiddlewareMixin):
    """
    Acceso al objecto request dentro de scopes como ser models y signals
    """
    def process_request(self, request):
        if request.user.is_authenticated:
            setattr(_thread_local, 'request', request)

    
def get_current_request():
    """
    obtiene el objeto request en cualquier scope que sea utilizado
    """
    return getattr(_thread_local, 'request', None)
