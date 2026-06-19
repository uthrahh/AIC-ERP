from django.urls import path
from reports.views import (
    reports_dashboard,
    startup_reports,
    service_reports,
    lab_reports,
    finance_reports,
    feedback_reports,
    export_startups_excel,
    export_startups_pdf,
)

app_name = 'reports'

urlpatterns = [
    path('', reports_dashboard, name='dashboard'),
    path('startups/', startup_reports, name='startups'),
    path('services/', service_reports, name='services'),
    path('labs/', lab_reports, name='labs'),
    path('finance/', finance_reports, name='finance'),
    path('feedback/', feedback_reports, name='feedback'),

    path(
        'startup/export/excel/',
        export_startups_excel,
        name='export_startups_excel'
    ),

    path(
        'startup/export/pdf/',
        export_startups_pdf,
        name='export_startups_pdf'
    ),
]
