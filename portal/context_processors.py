from django.conf import settings


def site_settings(request):
    return {
        'CIIC_CONTACT_PHONE': settings.CIIC_CONTACT_PHONE,
        'CIIC_CONTACT_EMAIL': settings.CIIC_CONTACT_EMAIL,
        'CIIC_OFFICE_ADDRESS': settings.CIIC_OFFICE_ADDRESS,
    }