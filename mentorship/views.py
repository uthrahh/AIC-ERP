from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from accounts.decorators import admin_required, startup_required, get_startup_for_user
from audit.utils import log_action
from mentorship.forms import MentorshipBookingForm, AdminMentorshipForm
from mentorship.models import MentorshipBooking
from portal.utils import acknowledge_action


@startup_required
def booking_create(request):
    startup = get_startup_for_user(request.user)
    if request.method == 'POST':
        form = MentorshipBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.startup = startup
            booking.bill_amount = booking.mentor.charges
            booking.save()
            log_action(request.user, 'mentorship_booking_created', 'mentorship', booking.pk, request=request)
            messages.success(request, 'Mentorship session requested.')
            return redirect('mentorship:list')
    else:
        form = MentorshipBookingForm()
    return render(request, 'mentorship/create.html', {'form': form, 'startup': startup})


@startup_required
def booking_list(request):
    startup = get_startup_for_user(request.user)
    bookings = startup.mentorship_bookings.select_related('mentor').all()
    return render(request, 'mentorship/booking_list.html', {'bookings': bookings})


@admin_required
def admin_list(request):
    bookings = MentorshipBooking.objects.select_related('startup', 'mentor')
    status = request.GET.get('status')
    if status:
        bookings = bookings.filter(status=status)
    return render(request, 'mentorship/admin_list.html', {
        'bookings': bookings,
        'status_filter': status,
    })


@admin_required
def admin_detail(request, pk):
    booking = get_object_or_404(MentorshipBooking, pk=pk)
    acknowledge_action(request.user, 'mentorship', pk)
    if request.method == 'POST':
        form = AdminMentorshipForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            log_action(request.user, f'mentorship_{booking.status}', 'mentorship', booking.pk, request=request)
            messages.success(request, 'Mentorship booking updated.')
            return redirect('mentorship:admin_detail', pk=pk)
    else:
        form = AdminMentorshipForm(instance=booking)
    return render(request, 'mentorship/admin_detail.html', {'booking': booking, 'form': form})
