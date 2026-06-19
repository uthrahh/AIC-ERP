from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from accounts.decorators import admin_required, startup_required, get_startup_for_user
from accounts.models import User
from audit.utils import log_action
from portal.utils import acknowledge_action
from services.forms import ServiceRequestForm, ServiceFeedbackForm, AdminServiceUpdateForm
from services.models import ServiceRequest, ServiceFeedback


@startup_required
def request_create(request):
    startup = get_startup_for_user(request.user)
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            sr = form.save(commit=False)
            sr.startup = startup
            sr.save()
            log_action(request.user, 'service_request_created', 'services', sr.pk, request=request)
            messages.success(request, 'Service request submitted.')
            return redirect('services:list')
    else:
        form = ServiceRequestForm()
    return render(request, 'services/create.html', {'form': form})


@startup_required
def request_list(request):
    startup = get_startup_for_user(request.user)

    if startup is None:
        return render(request, 'services/request_list.html', {
            'requests': ServiceRequest.objects.none()
        })

    requests = startup.service_requests.all()

    return render(request, 'services/request_list.html', {
        'requests': requests
    })


@startup_required
def request_feedback(request, pk):
    startup = get_startup_for_user(request.user)
    sr = get_object_or_404(ServiceRequest, pk=pk, startup=startup, status='Closed')
    if hasattr(sr, 'feedback'):
        messages.info(request, 'Feedback already submitted.')
        return redirect('services:list')
    if request.method == 'POST':
        form = ServiceFeedbackForm(request.POST)
        if form.is_valid():
            fb = form.save(commit=False)
            fb.request = sr
            fb.save()
            log_action(request.user, 'service_feedback_submitted', 'services', fb.pk, request=request)
            messages.success(request, 'Thank you for your feedback.')
            return redirect('services:list')
    else:
        form = ServiceFeedbackForm()
    return render(request, 'services/feedback.html', {'form': form, 'service_request': sr})


@admin_required
def admin_list(request):
    requests = ServiceRequest.objects.select_related('startup', 'assigned_to')
    status = request.GET.get('status')
    if status:
        requests = requests.filter(status=status)
    return render(request, 'services/admin_list.html', {
        'requests': requests,
        'status_filter': status,
        'statuses': ServiceRequest.Status.choices,
    })


@admin_required
def admin_detail(request, pk):
    sr = get_object_or_404(ServiceRequest, pk=pk)
    acknowledge_action(request.user, 'service', pk)
    if request.method == 'POST':
        form = AdminServiceUpdateForm(request.POST, instance=sr)
        if form.is_valid():
            sr = form.save(commit=False)
            if sr.status == ServiceRequest.Status.CLOSED and not sr.closed_at:
                sr.closed_at = timezone.now()
            sr.save()
            log_action(request.user, f'service_status_{sr.status}', 'services', sr.pk, request=request)
            messages.success(request, 'Request updated.')
            return redirect('services:admin_detail', pk=pk)
    else:
        form = AdminServiceUpdateForm(instance=sr)
    return render(request, 'services/admin_detail.html', {
        'service_request': sr,
        'form': form,
        'admins': User.objects.filter(role='admin'),
    })
