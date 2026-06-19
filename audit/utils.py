from audit.models import AuditLog


def log_action(user, action, module, object_id='', details='', request=None):
    ip = None
    if request:
        ip = getattr(request, 'audit_ip', None)
    AuditLog.objects.create(
        user=user if user and user.is_authenticated else None,
        action=action,
        module=module,
        object_id=str(object_id) if object_id else '',
        details=details,
        ip_address=ip,
    )
