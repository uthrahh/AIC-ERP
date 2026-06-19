from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Complaint(models.Model):
    class Status(models.TextChoices):
        OPEN = 'open', 'Open'
        IN_PROGRESS = 'in_progress', 'In Progress'
        CLOSED = 'closed', 'Closed'

    startup = models.ForeignKey(
        'startups.Startup', on_delete=models.CASCADE, related_name='complaints'
    )
    subject = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'complaints'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.subject} - {self.startup.brand_name}'


class GeneralFeedback(models.Model):
    class FeedbackType(models.TextChoices):
        PORTAL = 'portal', 'Portal Experience'
        SERVICE = 'service', 'General Service'
        INCUBATION = 'incubation', 'Incubation Support'
        OTHER = 'other', 'Other'

    startup = models.ForeignKey(
        'startups.Startup', on_delete=models.CASCADE, related_name='general_feedback'
    )
    feedback_type = models.CharField(max_length=20, choices=FeedbackType.choices, default=FeedbackType.PORTAL)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comments = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'general_feedback'
        ordering = ['-submitted_at']

    def __str__(self):
        return f'Feedback from {self.startup.brand_name}'
