from django.db import models


class NotificationQueue(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Sent', 'Sent'),
        ('Failed', 'Failed'),
    ]

    startup = models.ForeignKey(
        'startups.Startup',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    recipient_email = models.EmailField()

    subject = models.CharField(max_length=255)

    message = models.TextField()

    scheduled_at = models.DateTimeField()

    sent_at = models.DateTimeField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    class Meta:
        db_table = 'notification_queue'