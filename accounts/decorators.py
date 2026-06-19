from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped(request, *args, **kwargs):
            user = request.user
            if user.is_superuser or user.role in roles:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return _wrapped
    return decorator


def admin_required(view_func):
    return role_required('admin')(view_func)


def startup_required(view_func):
    return role_required('startup')(view_func)


def mentor_required(view_func):
    return role_required('mentor')(view_func)


def get_startup_for_user(user):
    if user.is_authenticated and user.startup_id:
        return user.startup
    return None


def get_mentor_for_user(user):
    if user.is_authenticated and user.mentor_id:
        return user.mentor
    return None
