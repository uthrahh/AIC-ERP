from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from accounts.decorators import admin_required, startup_required, get_startup_for_user
from audit.utils import log_action
from portal.utils import acknowledge_action
from labs.forms import LabBookingForm, AdminLabBookingForm
from labs.models import LabBooking, BookingEquipment


@startup_required
def booking_create(request):
    startup = get_startup_for_user(request.user)
    if request.method == 'POST':
        form = LabBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.startup = startup
            booking.save()
            for eq in form.cleaned_data.get('equipment', []):
                BookingEquipment.objects.create(booking=booking, equipment=eq)
            log_action(request.user, 'lab_booking_created', 'labs', booking.pk, request=request)
            messages.success(request, 'Lab booking request submitted.')
            return redirect('labs:list')
    else:
        form = LabBookingForm()
    return render(request, 'labs/create.html', {'form': form})


@startup_required
def booking_list(request):
    startup = get_startup_for_user(request.user)

    if startup is None:
        return render(request, 'labs/booking_list.html', {
            'bookings': LabBooking.objects.none()
        })

    bookings = startup.lab_bookings.select_related('lab').all()

    return render(request, 'labs/booking_list.html', {
        'bookings': bookings
    })


@admin_required
def admin_list(request):
    bookings = LabBooking.objects.select_related('startup', 'lab')
    status = request.GET.get('status')
    if status:
        bookings = bookings.filter(status=status)
    return render(request, 'labs/admin_list.html', {
        'bookings': bookings,
        'status_filter': status,
        'statuses': LabBooking.Status.choices,
    })


@admin_required
def admin_detail(request, pk):
    booking = get_object_or_404(LabBooking, pk=pk)
    acknowledge_action(request.user, 'lab', pk)
    if request.method == 'POST':
        form = AdminLabBookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            log_action(request.user, f'lab_booking_{booking.status}', 'labs', booking.pk, request=request)
            messages.success(request, 'Booking updated.')
            return redirect('labs:admin_detail', pk=pk)
    else:
        form = AdminLabBookingForm(instance=booking)
    equipment = booking.equipment_items.select_related('equipment')
    return render(request, 'labs/admin_detail.html', {
        'booking': booking,
        'form': form,
        'equipment': equipment,
    })
