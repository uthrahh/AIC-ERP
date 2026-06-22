from django.db import models
from django.contrib.auth.models import AbstractUser

ROLE_CHOICES = [
    ('ADMIN', 'Admin'),
    ('MENTOR', 'Mentor'),
    ('STARTUP', 'Startup'),
    ('APPLICANT', 'Applicant'),
]

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        STARTUP = "startup", "Startup User"
        MENTOR = "mentor", "Mentor"
        APPLICANT = "applicant", "Applicant"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STARTUP)
    startup = models.ForeignKey(
        'startups.Startup',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='users',
    )
    mentor = models.ForeignKey(
        'mentors.Mentor',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='users',
    )
    phone = models.CharField(max_length=20, blank=True)
    last_login_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    @property
    def is_applicant(self):
        return self.role == self.Role.APPLICANT
        
    @property
    def is_startup_user(self):
        return self.role == self.Role.STARTUP

    @property
    def is_mentor_user(self):
        return self.role == self.Role.MENTOR
    

