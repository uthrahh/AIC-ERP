from django.db import models

class Hall(models.Model):

    hall_name = models.CharField(max_length=255)

    hall_code = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        unique=True
    )

    capacity = models.PositiveIntegerField(default=1)

    location = models.CharField(
        max_length=255,
        blank=True
    )

    active = models.BooleanField(default=True)

    def __str__(self):
        return self.hall_name


class HallBooking(models.Model):

    class Status(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        APPROVED = 'Approved', 'Approved'
        REJECTED = 'Rejected', 'Rejected'
        COMPLETED = 'Completed', 'Completed'

    startup = models.ForeignKey(
        'startups.Startup',
        on_delete=models.CASCADE,
        related_name='conference_hall_bookings'
    )

    event_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    hall = models.ForeignKey(
        Hall,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    booking_date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    attendees = models.PositiveIntegerField(default=1)

    utilities_required = models.JSONField(default=list)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)