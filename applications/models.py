from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

SERVICE_CHOICES = [
    ('Mentorship', 'Mentorship'),
    ('Funding', 'Funding'),
    ('Market Connect', 'Market Connect'),
    ('Machinery', 'Machinery'),
    ('Others', 'Others'),
]

class Application(models.Model):
    class Status(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        COMPLETE = 'Complete', 'Complete'
        UNDER_REVIEW = 'Under Review', 'Under Review'
        ON_HOLD = 'On Hold', 'On Hold'
        APPROVED = 'Approved', 'Approved'
        REJECTED = 'Rejected', 'Rejected'

    timestamp = models.DateTimeField(auto_now_add=True)
    founder_name = models.CharField(max_length=50)
    startup_name = models.CharField(max_length=30)
    building_name = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6)
    area = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    problem_statement = models.CharField(max_length=500)
    solution = models.CharField(max_length=500)
    services_required = models.JSONField(default=list)
    other_service = models.CharField(max_length=50, blank=True)
    reference_source = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    class Meta:
        db_table = 'applications'
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.startup_name} - {self.status}'

    @property
    def services_required_display(self):
        items = list(self.services_required)

        if self.other_service:
            items.append(f"Others: {self.other_service}")

        return ", ".join(items)


class ApplicationReview(models.Model):
    application = models.OneToOneField(
        Application, on_delete=models.CASCADE, related_name='review'
    )
    innovation_score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)], null=True, blank=True
    )
    commercialization_score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)], null=True, blank=True
    )
    feasibility_score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)], null=True, blank=True
    )
    comments = models.TextField(blank=True)
    hod_name = models.CharField(max_length=255, blank=True)
    department = models.CharField(max_length=255, blank=True)
    reviewed_by = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL, null=True, related_name='application_reviews'
    )
    reviewed_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'application_reviews'

    def __str__(self):
        return f'Review for {self.application.startup_name}'

class ApplicationMentorshipReview(models.Model):

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='mentor_reviews'
    )

    mentor = models.ForeignKey(
        'mentors.Mentor',
        on_delete=models.SET_NULL,
        null=True
    )

    comments = models.TextField()

    review_date = models.DateField()

    class Meta:
        db_table = 'application_mentor_reviews'
