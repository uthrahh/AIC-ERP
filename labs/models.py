from django.db import models
from django.utils import timezone

class Lab(models.Model):

    lab_name = models.CharField(max_length=255)

    lab_code = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True
    )

    location = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    capacity = models.PositiveIntegerField(default=1)

    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'labs'

    def __str__(self):
        return self.lab_name


class Equipment(models.Model):

    class Availability(models.TextChoices):
        AVAILABLE = 'available', 'Available'
        IN_USE = 'in_use', 'In Use'
        MAINTENANCE = 'maintenance', 'Maintenance'

    lab = models.ForeignKey(
        Lab,
        on_delete=models.CASCADE,
        related_name='equipment'
    )

    equipment_name = models.CharField(
        max_length=255
    )

    equipment_code = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True
    )

    description = models.TextField(
        blank=True
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    tariff = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    availability_status = models.CharField(
        max_length=20,
        choices=Availability.choices,
        default=Availability.AVAILABLE
    )

    active = models.BooleanField(
        default=True
    )

    class Meta:
        db_table = "equipment"

    def __str__(self):
        return self.equipment_name

class LabBooking(models.Model):

    class Status(models.TextChoices):
        NEW = 'New', 'New'
        UNDER_REVIEW = 'Under Review', 'Under Review'
        APPROVED = 'Approved', 'Approved'
        REJECTED = 'Rejected', 'Rejected'
        CLOSED = 'Closed', 'Closed'

    startup = models.ForeignKey(
        'startups.Startup',
        on_delete=models.CASCADE,
        related_name='lab_bookings'
    )

    lab = models.ForeignKey(
        Lab,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    booking_title = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    purpose = models.TextField(
        blank=True
    )

    requested_date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    startup_members = models.PositiveIntegerField(
        default=1
    )

    tariff_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    invoice_generated = models.BooleanField(
        default=False
    )

    invoice = models.ForeignKey(
        'finance.Invoice',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    remarks = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = 'lab_bookings'

    def __str__(self):
        return f'{self.lab.lab_name} - {self.status}'


class BookingEquipment(models.Model):

    booking = models.ForeignKey(
        LabBooking,
        on_delete=models.CASCADE,
        related_name='equipment_items'
    )

    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    tariff_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    class Meta:
        db_table = 'booking_equipment'

    def __str__(self):
        return f'{self.booking.id} - {self.equipment.equipment_name}'


class EquipmentImportLog(models.Model):

    uploaded_file = models.FileField(
        upload_to='labs/imports/'
    )

    imported_at = models.DateTimeField(
        auto_now_add=True
    )

    imported_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        db_table = 'equipment_import_logs'


class LabTariffTemplate(models.Model):

    lab = models.ForeignKey(
        Lab,
        on_delete=models.CASCADE
    )

    base_charge = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    hourly_charge = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    class Meta:
        db_table = 'lab_tariff_templates'

class EquipmentMaster(models.Model):

    applicant_centre = models.CharField(
        max_length=255
    )

    pan_number = models.CharField(
        max_length=50,
        blank=True
    )

    equipment_name = models.CharField(
        max_length=255
    )

    brand_name = models.CharField(
        max_length=255,
        blank=True
    )

    procurement_date = models.DateField(
        null=True,
        blank=True
    )

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "equipment_master"

    def __str__(self):
        return self.equipment_name