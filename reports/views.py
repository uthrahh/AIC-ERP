from django.db.models import Count, Sum, Avg
from django.db.models.functions import ExtractYear
from django.shortcuts import render

from accounts.decorators import admin_required
from applications.models import Application
from feedback.models import Complaint, GeneralFeedback
from finance.models import Invoice, Payment
from labs.models import LabBooking
from services.models import ServiceRequest, ServiceFeedback
from startups.models import Startup
from django.http import HttpResponse

from openpyxl import Workbook

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle
)

from reportlab.lib import colors


@admin_required
def reports_dashboard(request):
    return render(request, 'reports/dashboard.html', {
        'startup_stats': _startup_stats(),
        'service_stats': _service_stats(),
        'lab_stats': _lab_stats(),
        'finance_stats': _finance_stats(),
        'feedback_stats': _feedback_stats(),
    })


@admin_required
def startup_reports(request):
    startups = Startup.objects.all()
    sector_data = list(
        startups.exclude(sector='').values('sector').annotate(count=Count('id')).order_by('-count')
    )
    year_data = list(
        startups.exclude(onboarding_date__isnull=True)
        .annotate(year=ExtractYear('onboarding_date'))
        .values('year')
        .annotate(count=Count('id'))
        .order_by('year')
    )
    return render(request, 'reports/startup_reports.html', {
        'active_count': startups.filter(startup_status='Active').count(),
        'incubated_count': startups.filter(startup_status='Incubated').count(),
        'sector_data': sector_data,
        'year_data': year_data,
        'startups': startups[:50],
    })


@admin_required
def service_reports(request):
    requests = ServiceRequest.objects.all()
    closed = requests.filter(status='Closed', closed_at__isnull=False)
    avg_resolution = None
    if closed.exists():
        durations = [(r.closed_at - r.created_at).total_seconds() / 3600 for r in closed[:100]]
        avg_resolution = sum(durations) / len(durations) if durations else None
    return render(request, 'reports/service_reports.html', {
        'total_requests': requests.count(),
        'open_tickets': requests.exclude(status='Closed').count(),
        'avg_resolution_hours': round(avg_resolution, 1) if avg_resolution else 'N/A',
        'by_type': list(requests.values('service_type').annotate(count=Count('id'))),
        'by_status': list(requests.values('status').annotate(count=Count('id'))),
    })


@admin_required
def lab_reports(request):
    bookings = LabBooking.objects.all()
    return render(request, 'reports/lab_reports.html', {
        'total_bookings': bookings.count(),
        'approved': bookings.filter(status='Approved').count(),
        'by_lab': list(bookings.values('lab__lab_name').annotate(count=Count('id'))),
        'by_status': list(bookings.values('status').annotate(count=Count('id'))),
        'recent': bookings.select_related('startup', 'lab')[:20],
    })


@admin_required
def finance_reports(request):
    invoices = Invoice.objects.all()
    payments = Payment.objects.all()
    return render(request, 'reports/finance_reports.html', {
        'invoices_generated': invoices.count(),
        'total_invoiced': invoices.aggregate(t=Sum('amount'))['t'] or 0,
        'total_received': payments.aggregate(t=Sum('amount_paid'))['t'] or 0,
        'outstanding': sum(i.balance_due for i in invoices),
        'by_status': list(invoices.values('status').annotate(count=Count('id'), total=Sum('amount'))),
    })


@admin_required
def feedback_reports(request):
    service_fb = ServiceFeedback.objects.all()
    general_fb = GeneralFeedback.objects.all()
    return render(request, 'reports/feedback_reports.html', {
        'service_avg_rating': service_fb.aggregate(a=Avg('rating'))['a'],
        'general_avg_rating': general_fb.aggregate(a=Avg('rating'))['a'],
        'by_type': list(general_fb.values('feedback_type').annotate(avg=Avg('rating'), count=Count('id'))),
        'recent_general': general_fb.select_related('startup')[:20],
    })


def _startup_stats():
    return {
        'total': Startup.objects.count(),
        'active': Startup.objects.filter(startup_status='Active').count(),
    }


def _service_stats():
    return {
        'total': ServiceRequest.objects.count(),
        'open': ServiceRequest.objects.exclude(status='Closed').count(),
    }


def _lab_stats():
    return {'total': LabBooking.objects.count(), 'pending': LabBooking.objects.filter(status='New').count()}


def _finance_stats():
    return {
        'invoices': Invoice.objects.count(),
        'outstanding': sum(i.balance_due for i in Invoice.objects.all()[:500]),
    }


def _feedback_stats():
    return {'avg_rating': GeneralFeedback.objects.aggregate(a=Avg('rating'))['a']}

def export_startups_excel(request):

    wb = Workbook()

    ws = wb.active

    ws.title = "Startups"

    ws.append([
        "Startup Code",
        "Brand Name",
        "Sector",
        "Status",
        "Funding Stage",
        "Valuation"
    ])

    for s in Startup.objects.all():

        ws.append([
            s.startup_code,
            s.brand_name,
            s.sector,
            s.startup_status,
            s.funding_stage,
            float(s.startup_valuation or 0)
        ])

    response = HttpResponse(
        content_type=
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    response[
        'Content-Disposition'
    ] = 'attachment; filename=startups.xlsx'

    wb.save(response)

    return response

def export_startups_pdf(request):

    response = HttpResponse(
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = 'attachment; filename=startups.pdf'

    doc = SimpleDocTemplate(response)

    data = [[
        'Code',
        'Brand',
        'Sector',
        'Status'
    ]]

    for s in Startup.objects.all():

        data.append([
            s.startup_code,
            s.brand_name,
            s.sector,
            s.startup_status
        ])

    table = Table(data)

    table.setStyle(
        TableStyle([
            ('GRID',(0,0),(-1,-1),1,colors.black),
            ('BACKGROUND',(0,0),(-1,0),colors.lightgrey),
        ])
    )

    doc.build([table])

    return response