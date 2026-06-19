from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class ServiceRequest(models.Model):
    class ServiceType(models.TextChoices):
        ELECTRICITY = 'Electricity', 'Electricity'
        AC = 'AC', 'AC'
        MANPOWER = 'Manpower', 'Manpower'
        OTHERS = 'Others', 'Others'

    class Status(models.TextChoices):
        NEW = 'New', 'New'
        UNDER_REVIEW = 'Under Review', 'Under Review'
        PROCESSING = 'Processing', 'Processing'
        CLOSED = 'Closed', 'Closed'

    startup = models.ForeignKey(
        'startups.Startup', on_delete=models.CASCADE, related_name='service_requests'
    )
    service_type = models.CharField(max_length=50, choices=ServiceType.choices)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    closed_at = models.DateTimeField(null=True, blank=True)
    assigned_to = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_service_requests',
    )

    class Meta:
        db_table = 'service_requests'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.service_type} - {self.startup.brand_name} ({self.status})'


class ServiceFeedback(models.Model):
    request = models.OneToOneField(
        ServiceRequest, on_delete=models.CASCADE, related_name='feedback'
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comments = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'service_feedback'

    def __str__(self):
        return f'Feedback for request #{self.request_id}'

class ServiceCategory(models.Model):

    service_name = models.CharField(max_length=255)

    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'service_categories'


class ServiceTariff(models.Model):

    service = models.ForeignKey(
        ServiceCategory,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    class Meta:
        db_table = 'service_tariffs'