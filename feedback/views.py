from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from accounts.decorators import admin_required, startup_required, get_startup_for_user
from audit.utils import log_action
from portal.utils import acknowledge_action
from feedback.forms import ComplaintForm, GeneralFeedbackForm, AdminComplaintForm
from feedback.models import Complaint, GeneralFeedback


@startup_required
def complaint_create(request):
    startup = get_startup_for_user(request.user)
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.startup = startup
            complaint.save()
            log_action(request.user, 'complaint_created', 'feedback', complaint.pk, request=request)
            messages.success(request, 'Complaint submitted.')
            return redirect('feedback:complaint_list')
    else:
        form = ComplaintForm()
    return render(request, 'feedback/complaint_form.html', {'form': form})


@startup_required
def complaint_list(request):
    startup = get_startup_for_user(request.user)
    complaints = startup.complaints.all()
    return render(request, 'feedback/complaint_list.html', {'complaints': complaints})


@startup_required
def feedback_submit(request):
    startup = get_startup_for_user(request.user)
    if request.method == 'POST':
        form = GeneralFeedbackForm(request.POST)
        if form.is_valid():
            fb = form.save(commit=False)
            fb.startup = startup
            fb.save()
            log_action(request.user, 'feedback_submitted', 'feedback', fb.pk, request=request)
            messages.success(request, 'Feedback submitted. Thank you!')
            return redirect('portal:startup_home')
    else:
        form = GeneralFeedbackForm()
    return render(request, 'feedback/feedback_form.html', {'form': form})


@admin_required
def admin_complaint_list(request):
    complaints = Complaint.objects.select_related('startup')
    return render(request, 'feedback/admin_complaint_list.html', {'complaints': complaints})


@admin_required
def admin_complaint_detail(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    acknowledge_action(request.user, 'complaint', pk)
    if request.method == 'POST':
        form = AdminComplaintForm(request.POST, instance=complaint)
        if form.is_valid():
            complaint = form.save(commit=False)
            if complaint.status == Complaint.Status.CLOSED and not complaint.closed_at:
                complaint.closed_at = timezone.now()
            complaint.save()
            log_action(request.user, 'complaint_updated', 'feedback', complaint.pk, request=request)
            messages.success(request, 'Complaint updated.')
            return redirect('feedback:admin_complaint_list')
    else:
        form = AdminComplaintForm(instance=complaint)
    return render(request, 'feedback/admin_complaint_detail.html', {'complaint': complaint, 'form': form})
