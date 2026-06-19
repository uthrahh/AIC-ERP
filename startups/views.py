from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView
from startups.forms import (
    StartupProfileForm,
    AdminStartupForm,
    DocumentUploadForm,
    TeamMemberForm,
    StartupMediaForm,
    FounderForm,
    FundingForm,
    LoanForm,
    AwardForm,
    IPRForm,
    EmployeeForm,
    BankAccountForm,
    QuarterlyUpdateForm,
)
from accounts.decorators import admin_required, startup_required, get_startup_for_user
from accounts.forms import AdminCreateStartupUserForm
from audit.utils import log_action
from startups.models import (
    Startup,
    Document,
    StartupTeamMember,
    StartupMedia,
    Founder,
    StartupFunding,
    StartupLoan,
    StartupAward,
    StartupIPR,
    StartupEmployee,
    StartupBankAccount,
    QuarterlyFinancialUpdate,
)
User = get_user_model()

@startup_required
def profile_setup(request):
    startup = get_startup_for_user(request.user)
    if request.method == 'POST':
        form = StartupProfileForm(request.POST, request.FILES, instance=startup)
        if form.is_valid():
            startup = form.save(commit=False)
            startup.save()
            log_action(request.user, 'profile_completed', 'startups', startup.pk, request=request)
            messages.success(request, 'Profile created successfully.')
            return redirect('portal:startup_home')
    else:
        form = StartupProfileForm(instance=startup)
    return render(request, 'startups/profile_setup.html', {'form': form, 'startup': startup})


@startup_required
def profile_view(request):
    startup = get_startup_for_user(request.user)
    return render(request, 'startups/profile.html', {
        'startup': startup,
        'documents': startup.documents.all(),
        'team_members': startup.team_members.all(),
        'media_items': startup.media.all(),
        'service_logs': startup.service_requests.filter(status='Closed'),
        'lab_history': startup.lab_bookings.filter(status__in=['Approved', 'Closed']),
        'invoices': startup.invoices.all()[:10],
    })


@startup_required
def profile_edit(request):
    startup = get_startup_for_user(request.user)
    if request.method == 'POST':
        form = StartupProfileForm(request.POST, request.FILES, instance=startup)
        if form.is_valid():
            form.save()
            log_action(request.user, 'profile_updated', 'startups', startup.pk, request=request)
            messages.success(request, 'Profile updated.')
            return redirect('startups:profile')
    else:
        form = StartupProfileForm(instance=startup)
    return render(request, 'startups/profile_edit.html', {'form': form})


@startup_required
def document_upload(request):
    startup = get_startup_for_user(request.user)
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.startup = startup
            doc.uploaded_by = request.user
            doc.save()
            log_action(request.user, 'document_uploaded', 'documents', doc.pk, request=request)
            messages.success(request, 'Document uploaded.')
            return redirect('startups:profile')
    else:
        form = DocumentUploadForm()
    return render(request, 'startups/document_upload.html', {'form': form})


@admin_required
def admin_startup_list(request):
    startups = Startup.objects.prefetch_related('founders').all()
    q = request.GET.get('q', '')
    status = request.GET.get('status', '')
    sector = request.GET.get('sector', '')
    funding_stage = request.GET.get('funding_stage', '')

    if q:
        startups = startups.filter(
            Q(brand_name__icontains=q) |
            Q(startup_code__icontains=q) |
            Q(primary_poc_name__icontains=q)
        )
    if status:
        startups = startups.filter(startup_status=status)
    if sector:
        startups = startups.filter(sector=sector)
    if funding_stage:
        startups = startups.filter(funding_stage=funding_stage)

    startups = startups.order_by('brand_name')
    paginator = Paginator(startups, 20)
    page = paginator.get_page(request.GET.get('page'))

    return render(request, 'startups/admin_list.html', {
        'startups': page,
        'q': q,
        'status': status,
        'sector': sector,
        'funding_stage': funding_stage,
    })


@admin_required
def admin_startup_create(request):
    user_form = AdminCreateStartupUserForm()
    startup_form = AdminStartupForm()
    if request.method == 'POST':
        user_form = AdminCreateStartupUserForm(request.POST)
        startup_form = AdminStartupForm(request.POST, request.FILES)
        if user_form.is_valid() and startup_form.is_valid():
            startup = startup_form.save()
            user = user_form.save(commit=False)
            user.startup = startup
            user.save()
            log_action(request.user, 'startup_created', 'startups', startup.pk, request=request)
            messages.success(
                request,
                f'Startup created. ID: {startup.startup_code}, Username: {user.username}',
            )
            return redirect('startups:admin_detail', pk=startup.pk)
    return render(request, 'startups/admin_create.html', {
        'user_form': user_form,
        'startup_form': startup_form,
    })


@admin_required
def admin_startup_detail(request, pk):
    startup = get_object_or_404(Startup, pk=pk)
    return render(request, 'startups/admin_detail.html', {
        'startup': startup,
        'users': startup.users.all(),
        'documents': startup.documents.all(),
        'service_requests': startup.service_requests.all()[:20],
        'invoices': startup.invoices.all(),
    })


@admin_required
def admin_startup_edit(request, pk):
    startup = get_object_or_404(Startup, pk=pk)
    if request.method == 'POST':
        form = AdminStartupForm(request.POST, request.FILES, instance=startup)
        if form.is_valid():
            form.save()
            log_action(request.user, 'startup_updated', 'startups', startup.pk, request=request)
            messages.success(request, 'Startup updated.')
            return redirect('startups:admin_detail', pk=pk)
    else:
        form = AdminStartupForm(instance=startup)
    return render(request, 'startups/admin_edit.html', {'form': form, 'startup': startup})


class StartupPublicDetailView(DetailView):
    model = Startup
    template_name = 'startups/public_detail.html'
    context_object_name = 'startup'

    def get_queryset(self):
        return Startup.objects.filter(
            startup_status__in=['active', 'graduated']
        )

@startup_required
def founder_create(request):

    startup = get_startup_for_user(request.user)

    if request.method == "POST":

        form = FounderForm(request.POST)

        if form.is_valid():

            founder = form.save(commit=False)
            founder.startup = startup
            founder.save()

            messages.success(request, "Founder added.")

            return redirect("startups:profile")

    else:

        form = FounderForm()

    return render(
        request,
        "startups/founder_form.html",
        {
            "form": form,
            "title": "Add Founder"
        }
    )