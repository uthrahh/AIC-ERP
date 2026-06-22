from django.conf import settings
from applications.models import Application
from services.models import ServiceRequest
from labs.models import LabBooking
from halls.models import HallBooking
from feedback.models import Complaint
from portal.utils import filter_unacknowledged


def admin_notifications(request):

    if not request.user.is_authenticated:
        return {}

    if not getattr(request.user, "is_admin", False):
        return {}

    pending_apps = filter_unacknowledged(
        request.user,
        "application",
        Application.objects.filter(
            status__in=[
                "Complete",
                "Pending",
                "Under Review",
                "On Hold",
            ]
        ),
    )

    pending_services = filter_unacknowledged(
        request.user,
        "service",
        ServiceRequest.objects.filter(status="New"),
    )

    pending_labs = filter_unacknowledged(
        request.user,
        "lab",
        LabBooking.objects.filter(status="New"),
    )

    pending_halls = filter_unacknowledged(
        request.user,
        "hall",
        HallBooking.objects.filter(status="Pending"),
    )

    pending_complaints = filter_unacknowledged(
        request.user,
        "complaint",
        Complaint.objects.filter(status="open"),
    )

    return {
        "new_applications_count": pending_apps.count(),
        "new_service_count": pending_services.count(),
        "new_lab_count": pending_labs.count(),
        "new_hall_count": pending_halls.count(),
        "new_complaint_count": pending_complaints.count(),
    }


def site_settings(request):
    return {
        'CIIC_CONTACT_PHONE': settings.CIIC_CONTACT_PHONE,
        'CIIC_CONTACT_EMAIL': settings.CIIC_CONTACT_EMAIL,
        'CIIC_OFFICE_ADDRESS': settings.CIIC_OFFICE_ADDRESS,
    }