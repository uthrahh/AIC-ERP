from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from accounts.decorators import admin_required
from applications.forms import ApplicationForm, ApplicationReviewForm
from applications.models import Application, ApplicationReview
from audit.utils import log_action
from portal.utils import acknowledge_action
from django.contrib.auth.decorators import login_required

@login_required
def application_submit(request):

    print("VIEW HIT")

    if Application.objects.filter(
        user=request.user
    ).exists():

        messages.warning(
            request,
            "You have already submitted an application."
        )

        return redirect("applicants:dashboard")

    if request.method == "POST":

        form = ApplicationForm(request.POST)

        print("POST RECEIVED")

        if form.is_valid():

            print("FORM VALID")

            app = form.save(commit=False)
            app.user = request.user
            app.status = Application.Status.COMPLETE
            app.save()

            messages.success(
                request,
                "Application submitted successfully! We'll get back to you soon."
            )

            return redirect(
                "applications:submit_success",
                pk=app.pk
            )

        else:

            print("FORM INVALID")
            print(form.errors)

    else:

        form = ApplicationForm()

    return render(
        request,
        "applications/submit.html",
        {
            "form": form
        }
    )

def application_success(request, pk):

    print("SUCCESS PAGE HIT")

    application = get_object_or_404(
        Application,
        pk=pk
    )

    return render(
        request,
        'applications/success.html',
        {
            'application': application
        }
    )


@admin_required
def admin_application_list(request):
    applications = Application.objects.all()
    status = request.GET.get('status')
    if status:
        applications = applications.filter(status=status)
    return render(request, 'applications/admin_list.html', {
        'applications': applications,
        'status_filter': status,
        'sector_filter': '',
        'statuses': Application.Status.choices,
    })


@admin_required
def admin_application_detail(request, pk):
    application = get_object_or_404(Application, pk=pk)
    acknowledge_action(request.user, 'application', pk)
    review, _ = ApplicationReview.objects.get_or_create(application=application)
    if request.method == 'POST':
        form = ApplicationReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewed_by = request.user
            review.save()
            new_status = request.POST.get('status')
            if new_status:
                old_status = application.status
                application.status = new_status
                application.save()
                if new_status == Application.Status.APPROVED and old_status != Application.Status.APPROVED:
                    _send_approval_email(application)
                log_action(request.user, f'application_{new_status.lower()}', 'applications',
                           application.pk, request=request)
            messages.success(request, 'Review saved.')
            return redirect('applications:admin_detail', pk=pk)
    else:
        form = ApplicationReviewForm(instance=review, initial={'status': application.status})
    return render(request, 'applications/admin_detail.html', {
        'application': application,
        'review': review,
        'form': form,
        'status_choices': Application.Status.choices,
        'current_status': application.status,
    })


@admin_required
def admin_application_print(request, pk):
    application = get_object_or_404(Application, pk=pk)
    review = getattr(application, 'review', None)
    return render(request, 'applications/print.html', {
        'application': application,
        'review': review,
    })


def _send_approval_email(application):
    subject = f'Congratulations! Application Approved - {application.startup_name}'
    body = render_to_string('applications/emails/approval.txt', {'application': application})
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [application.email], fail_silently=True)

