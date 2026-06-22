import json
from decimal import Decimal
from django.core.paginator import Paginator
from django.db.models import Count, Sum, Q
from django.shortcuts import render
from django.db.models import Sum
from accounts.decorators import admin_required, startup_required, get_startup_for_user
from applications.models import Application
from content.models import GalleryItem, ServiceOffering, IncubationStep, Sponsor
from feedback.models import Complaint, GeneralFeedback
from finance.models import Invoice
from halls.models import HallBooking
from labs.models import LabBooking
from mentorship.models import MentorshipBooking
from portal.utils import filter_unacknowledged
from services.models import ServiceRequest
from startups.models import (
    Startup, StartupFunding, StartupAward, StartupIPR,
)
from startups.models import Startup
from django.db.models import Count


ACTIVE_STATUSES = ['active']
PUBLIC_STATUSES = ['active', 'graduated']


def home(request):
    startups = Startup.objects.filter(startup_status__in=ACTIVE_STATUSES)
    return render(request, 'portal/home.html', {
        'startup_count': startups.count(),
        'featured_startups': startups[:8],
    })


def about(request):

    items = list(GalleryItem.objects.filter(is_active=True))

    if len(items) < 10:
        placeholders = _placeholder_gallery()
        items = items + placeholders[:10 - len(items)]

    row1 = items[:5] + items[:5]
    row2 = items[5:10] + items[5:10]

    return render(request, 'portal/about.html', {
        'services': ServiceOffering.objects.filter(is_active=True),
        'steps': IncubationStep.objects.filter(is_active=True),
        'row1': row1,
        'row2': row2,
    })


def startup_directory(request):

    startups = Startup.objects.all()

    search = request.GET.get("q")

    if search:
        startups = startups.filter(
            Q(brand_name__icontains=search) |
            Q(company_description__icontains=search)
        )
    
    paginator = Paginator(startups, 12)
    page_number = request.GET.get("page")
    startups = paginator.get_page(page_number)

    total_startups = Startup.objects.count()

    active_startups = Startup.objects.filter(
        startup_status="active"
    ).count()

    incubated_startups = Startup.objects.filter(
        startup_status__in=["active", "graduated"]
    ).count()

    domains = (
        Startup.objects
        .exclude(sector="")
        .values("sector")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    domain_labels = []
    domain_counts = []

    for d in domains:
        domain_labels.append(d["sector"])
        domain_counts.append(d["total"])

    active = Startup.objects.filter(startup_status='active')
    graduated = Startup.objects.filter(startup_status='graduated')

    govt_grants = StartupFunding.objects.filter(
        funding_type__in=['Government Grant', 'CSR Grant', 'Seed Fund']
    ).aggregate(t=Sum('amount'))['t'] or 0

    private_investment = StartupFunding.objects.filter(
        funding_type__in=['Angel Investment', 'VC Investment']
    ).aggregate(t=Sum('amount'))['t'] or 0

    awards_count = StartupAward.objects.count()

    jobs_created = active.aggregate(
        t=Sum('jobs_created')
    )['t'] or 0

    total_valuation = active.aggregate(
        t=Sum('startup_valuation')
    )['t'] or 0

    sales_turnover = active.aggregate(
        t=Sum('sales_turnover')
    )['t'] or 0

    funds_raised = StartupFunding.objects.aggregate(
        t=Sum('amount')
    )['t'] or 0

    total_funding = StartupFunding.objects.aggregate(
        t=Sum('amount')
    )['t'] or 0

    ipr_counts = {
        'patents': StartupIPR.objects.filter(ipr_type='Patent').count(),
        'trademarks': StartupIPR.objects.filter(ipr_type='Trademark').count(),
        'copyrights': StartupIPR.objects.filter(ipr_type='Copyright').count(),
        'design_rights': StartupIPR.objects.filter(ipr_type='Design Right').count(),
        'trade_secrets': StartupIPR.objects.filter(ipr_type='Trade Secret').count(),
    }

    ipr_counts['total'] = sum(ipr_counts.values())

    mentorship_sessions = MentorshipBooking.objects.filter(
        status='Completed'
    ).count()

    hall_events = HallBooking.objects.filter(
        status='Approved'
    ).count()

    lab_sessions = LabBooking.objects.filter(
        status='Approved'
    ).count()

    sector_data = list(
        active.exclude(sector='')
        .values('sector')
        .annotate(count=Count('id'))
        .order_by('-count')[:10]
    )

    sponsors = Sponsor.objects.filter(is_active=True)

    context = {

        "startups": startups,
        "search": search,
        "total_startups": total_startups,
        "active_startups": active_startups,
        "incubated_startups": incubated_startups,
        "total_funding": total_funding,
        "govt_grants": govt_grants,
        "private_investment": private_investment,
        "awards_count": awards_count,
        "jobs_created": jobs_created,
        "total_valuation": total_valuation,
        "sales_turnover": sales_turnover,
        "funds_raised": funds_raised,
        "active_count": active.count(),
        "graduated_count": graduated.count(),
        "incubated_total": active.count() + graduated.count(),
        "ipr_counts": ipr_counts,
        "mentorship_sessions": mentorship_sessions,
        "hall_events": hall_events,
        "lab_sessions": lab_sessions,
        "workshops": hall_events // 2,
        "networking_meetings": mentorship_sessions // 3,
        "total_meetings": mentorship_sessions + hall_events + lab_sessions,
        "partnerships": sponsors.count(),
        "builtup_area": 25000,
        "domains": domains,
        "domain_labels": json.dumps(domain_labels),
        "domain_counts": json.dumps(domain_counts),
        "sector_data_json": json.dumps(sector_data),
        "sponsors": sponsors,
    }

    return render(
        request,
        "portal/startup_directory.html",
        context,
    )

def contact(request):
    return render(request, 'portal/contact.html')

def team(request):
    return render(
        request,
        "portal/team.html"
    )


@startup_required
def startup_home(request):
    startup = get_startup_for_user(request.user)
    open_requests = startup.service_requests.exclude(status='Closed').count()
    open_complaints = startup.complaints.filter(status='open').count()
    pending_payments = startup.invoices.exclude(status='Paid').count()
    upcoming_labs = startup.lab_bookings.filter(
        status__in=['New', 'Approved']
    ).count()
    upcoming_halls = startup.conference_hall_bookings.filter(
        status__in=['Pending', 'Approved']
    ).count()
    recent_services = startup.service_requests.all()[:5]
    invoices = startup.invoices.all()
    total_billed = invoices.aggregate(t=Sum('amount'))['t'] or 0
    total_paid = sum(i.amount_paid for i in invoices)
    return render(request, 'portal/startup_home.html', {
        'startup': startup,
        'open_requests': open_requests,
        'open_complaints': open_complaints,
        'pending_payments': pending_payments,
        'upcoming_labs': upcoming_labs,
        'upcoming_halls': upcoming_halls,
        'recent_services': recent_services,
        'total_billed': total_billed,
        'total_paid': total_paid,
        'outstanding': total_billed - total_paid,
    })


@admin_required
def admin_home(request):
    user = request.user
    pending_apps = filter_unacknowledged(
        user, 'application',
        Application.objects.filter(status__in=['Complete', 'Pending', 'Under Review', 'On Hold'])
    )
    pending_services = filter_unacknowledged(
        user, 'service',
        ServiceRequest.objects.filter(status='New')
    )
    pending_labs = filter_unacknowledged(
        user, 'lab',
        LabBooking.objects.filter(status='New')
    )
    pending_halls = filter_unacknowledged(
        user, 'hall',
        HallBooking.objects.filter(status='Pending')
    )
    pending_complaints = filter_unacknowledged(
        user, 'complaint',
        Complaint.objects.filter(status='open')
    )
    pending_feedback = filter_unacknowledged(
        user,
        'feedback',
        GeneralFeedback.objects.all()
    )
    return render(request, 'portal/admin_home.html', {
        'pending_applications': pending_apps[:10],
        'pending_services': pending_services[:10],
        'pending_labs': pending_labs[:10],
        'pending_halls': pending_halls[:10],
        'pending_complaints': pending_complaints[:10],
        'pending_feedback': pending_feedback[:10],
        'new_applications_count': pending_apps.count(),
        'new_service_count': pending_services.count(),
        'new_lab_count': pending_labs.count(),
        'new_hall_count': pending_halls.count(),
        'new_complaint_count': pending_complaints.count(),
    })


@admin_required
def admin_history(request):
    return render(request, 'portal/admin_history.html', {
        'service_logs': ServiceRequest.objects.filter(status='Closed').select_related('startup')[:50],
        'lab_history': LabBooking.objects.filter(
            status__in=['Approved', 'Closed']
        ).select_related('startup', 'lab')[:50],
    })


def _placeholder_gallery():
    categories = ['Facilities', 'Events', 'Workspace']
    items = []
    for i in range(1, 11):
        items.append({
            'title': f'AIC-CIIC {categories[i % 3]} {i}',
            'description': f'Placeholder image — {categories[i % 3]}',
            'image': None,
            'category': categories[i % 3],
        })
    return items


def _placeholder_startups():
    domains = ['HealthTech', 'EdTech', 'AgriTech', 'FinTech', 'CleanTech', 'AI/ML', 'IoT', 'BioTech']
    items = []
    for i in range(1, 141):
        class Placeholder:
            pass
        s = Placeholder()
        s.pk = None
        s.brand_name = f'Startup {i:03d}'
        s.sector = domains[i % len(domains)]
        s.logo = None
        s.company_description = f'Innovating in {domains[i % len(domains)]}.'
        items.append(s)
    return items
