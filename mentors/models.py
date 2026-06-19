from django.db import models


class Mentor(models.Model):

    class MentorType(models.TextChoices):
        INTERNAL = 'Internal', 'Internal'
        EXTERNAL = 'External', 'External'

    mentor_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True
    )

    mentor_name = models.CharField(
        max_length=255
    )

    expertise = models.CharField(
        max_length=255
    )

    mentor_type = models.CharField(
        max_length=20,
        choices=MentorType.choices
    )

    charges = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    email = models.EmailField(
        blank=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.mentor_name