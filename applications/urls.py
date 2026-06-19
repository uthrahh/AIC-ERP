from django.urls import path
from applications.views import (
    application_submit, application_success,
    admin_application_list, admin_application_detail, admin_application_print,
)

app_name = 'applications'

urlpatterns = [
    path('submit/', application_submit, name='submit'),
    path('success/<int:pk>/', application_success, name='submit_success'),
    path('applications/manage/', admin_application_list, name='admin_list'),
    path('applications/manage/<int:pk>/', admin_application_detail, name='admin_detail'),
    path('applications/manage/<int:pk>/print/', admin_application_print, name='admin_print'),
]
