from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.urls import reverse


class ProfileRequiredMiddleware(MiddlewareMixin):
    """Force startup users to complete profile on first login."""

    EXEMPT_PREFIXES = (
        '/accounts/logout',
        '/accounts/login',
        '/accounts/password',
        '/startups/profile/setup',
        '/static/',
        '/media/',
        '/admin/',
    )

    def process_request(self, request):
        user = request.user
        if not user.is_authenticated:
            return None
        if user.role != 'startup' or not user.startup_id:
            return None
        path = request.path
        if any(path.startswith(p) for p in self.EXEMPT_PREFIXES):
            return None
        startup = user.startup
        if not startup.brand_name and not path.startswith('/startups/profile'):
            return redirect('startups:profile_setup')
        return None
