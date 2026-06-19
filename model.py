from django.db import models


class MentorshipBooking(models.Model):

    STATUS_CHOICES = [
        ('Requested', 'Requested'),
        ('Approved', 'Approved'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    startup = models.ForeignKey(
        'startups.Startup',
        on_delete=models.CASCADE
    )

    mentor = models.ForeignKey(
        'mentors.Mentor',
        on_delete=models.CASCADE
    )

    session_date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    bill_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Requested'
    )

    created_at = models.DateTimeField(auto_now_add=True)