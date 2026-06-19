from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404

from accounts.decorators import admin_required, startup_required, mentor_required, get_startup_for_user
from audit.utils import log_action
from finance.forms import InvoiceForm, PaymentForm
from finance.models import Invoice, Payment
from mentorship.models import MentorshipBooking


@startup_required
def billing_dashboard(request):
    startup = get_startup_for_user(request.user)
    invoices = startup.invoices.all()
    total_billed = invoices.aggregate(total=Sum('amount'))['total'] or 0
    total_paid = sum(inv.amount_paid for inv in invoices)
    return render(request, 'finance/startup_billing.html', {
        'invoices': invoices,
        'total_billed': total_billed,
        'total_paid': total_paid,
        'outstanding': total_billed - total_paid,
    })


@mentor_required
def mentor_billing(request):
    from accounts.decorators import get_mentor_for_user
    mentor = get_mentor_for_user(request.user)
    bookings = MentorshipBooking.objects.filter(
        mentor=mentor, status='Completed'
    ).select_related('startup')
    total_earned = sum(b.bill_amount for b in bookings)
    return render(request, 'finance/mentor_billing.html', {
        'bookings': bookings,
        'total_earned': total_earned,
        'mentor': mentor,
    })


@admin_required
def admin_invoice_list(request):
    invoices = Invoice.objects.select_related('startup')
    return render(request, 'finance/admin_invoice_list.html', {'invoices': invoices})


@admin_required
def admin_invoice_create(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save()
            log_action(request.user, 'invoice_created', 'finance', invoice.pk, request=request)
            messages.success(request, 'Invoice created.')
            return redirect('finance:admin_invoice_list')
    else:
        form = InvoiceForm()
    return render(request, 'finance/admin_invoice_form.html', {'form': form, 'title': 'Create Invoice'})


@admin_required
def admin_payment_record(request, invoice_pk):
    invoice = get_object_or_404(Invoice, pk=invoice_pk)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.invoice = invoice
            payment.save()
            if invoice.balance_due <= 0:
                invoice.status = 'Paid'
            elif invoice.amount_paid > 0:
                invoice.status = 'Partially Paid'
            invoice.save()
            log_action(request.user, 'payment_recorded', 'finance', payment.pk, request=request)
            messages.success(request, 'Payment recorded.')
            return redirect('finance:admin_invoice_list')
    else:
        form = PaymentForm()
    return render(request, 'finance/admin_payment_form.html', {'form': form, 'invoice': invoice})
