from django.utils.deprecation import MiddlewareMixin


class AuditMiddleware(MiddlewareMixin):
    EXEMPT_PREFIXES = ('/static/', '/media/', '/favicon')

    def process_request(self, request):
        request.audit_ip = self._get_client_ip(request)
        return None

    @staticmethod
    def _get_client_ip(request):
        x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded:
            return x_forwarded.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')
