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
        on_delete=models.CASCADE,
        related_name='mentorship_bookings'
    )

    mentor = models.ForeignKey(
        'mentors.Mentor',
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    session_date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    bill_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    notes = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Requested'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'mentorship_bookings'

    def __str__(self):
        return f'{self.startup.brand_name} - {self.mentor.mentor_name}'