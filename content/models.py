from django.db import models


class GalleryItem(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='gallery/')
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'gallery'
        ordering = ['display_order', '-created_at']
        verbose_name = 'Gallery item'

    def __str__(self):
        return self.title


class ServiceOffering(models.Model):
    """AIC-CIIC services listed on the About page."""
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'service_offerings'
        ordering = ['display_order']

    def __str__(self):
        return self.title


class IncubationStep(models.Model):
    step_number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'incubation_steps'
        ordering = ['step_number']

    def __str__(self):
        return f'Step {self.step_number}: {self.title}'


class Sponsor(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='sponsors/', blank=True, null=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'sponsors'

    def __str__(self):
        return self.name
