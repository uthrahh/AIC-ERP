from django.urls import path
from finance.views import (
    billing_dashboard, admin_invoice_list, admin_invoice_create, admin_payment_record,
    mentor_billing,
)

app_name = 'finance'

urlpatterns = [
    path('billing/', billing_dashboard, name='billing'),
    path('mentor/billing/', mentor_billing, name='mentor_billing'),
    path('manage/invoices/', admin_invoice_list, name='admin_invoice_list'),
    path('manage/invoices/create/', admin_invoice_create, name='admin_invoice_create'),
    path('manage/invoices/<int:invoice_pk>/payment/', admin_payment_record, name='admin_payment_record'),
]
