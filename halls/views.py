from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from accounts.decorators import admin_required, startup_required, get_startup_for_user
from audit.utils import log_action
from halls.forms import HallBookingForm, AdminHallBookingForm
from halls.models import HallBooking
from portal.utils import acknowledge_action


@startup_required
def booking_create(request):
    startup = get_startup_for_user(request.user)
    if request.method == 'POST':
        form = HallBookingForm(
            request.POST,
            attendees=request.POST.get('attendees'),
            booking_date=request.POST.get('booking_date'),
            start_time=request.POST.get('start_time'),
            end_time=request.POST.get('end_time'),
        )
        if form.is_valid():
            booking = form.save(commit=False)
            booking.startup = startup
            booking.save()
            log_action(request.user, 'hall_booking_created', 'halls', booking.pk, request=request)
            messages.success(request, 'Conference hall booking submitted.')
            return redirect('halls:list')
    else:
        form = HallBookingForm()
    return render(request, 'halls/create.html', {'form': form, 'startup': startup})


@startup_required
def booking_list(request):
    startup = get_startup_for_user(request.user)

    if startup is None:
        return render(request, 'halls/booking_list.html', {
            'bookings': HallBooking.objects.none()
        })

    bookings = startup.conference_hall_bookings.select_related('hall').all()

    return render(request, 'halls/booking_list.html', {
        'bookings': bookings
    })


@admin_required
def admin_list(request):
    bookings = HallBooking.objects.select_related(
        'startup',
        'hall'
    ).order_by(
        'booking_date',
        'start_time'
    ).order_by('booking_date', 'start_time')
    status = request.GET.get('status')
    if status:
        bookings = bookings.filter(status=status)
    return render(
        request,
        'halls/admin_list.html',
        {
            'bookings': bookings
        }
    )


@admin_required
def admin_detail(request, pk):
    booking = get_object_or_404(HallBooking, pk=pk)
    acknowledge_action(request.user, 'hall', pk)
    if request.method == 'POST':
        form = AdminHallBookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            log_action(request.user, f'hall_booking_{booking.status}', 'halls', booking.pk, request=request)
            messages.success(request, 'Booking updated.')
            return redirect('halls:admin_detail', pk=pk)
    else:
        form = AdminHallBookingForm(instance=booking)
    return render(request, 'halls/admin_detail.html', {
        'booking': booking,
        'form': form,
    })
