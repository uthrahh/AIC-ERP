from django.core.validators import MinValueValidator
from django.db.models import Sum

from django.db import models


class Invoice(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Partially Paid', 'Partially Paid'),
        ('Paid', 'Paid'),
        ('Overdue', 'Overdue'),
    ]

    startup = models.ForeignKey(
        'startups.Startup',
        on_delete=models.CASCADE,
        related_name='invoices'
    )

    invoice_number = models.CharField(
        max_length=50,
        unique=True
    )

    invoice_type = models.CharField(
        max_length=100,
        blank=True,
        default=''
    )

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    due_date = models.DateField()

    issued_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    remarks = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'invoices'
        ordering = ['-issued_date']

    def __str__(self):
        return self.invoice_number

    @property
    def amount_paid(self):
        total = self.payments.aggregate(total=Sum('amount_paid'))['total']
        return total or 0

    @property
    def balance_due(self):
        return self.amount - self.amount_paid


class Payment(models.Model):

    PAYMENT_METHODS = [
        ('UPI', 'UPI'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Card', 'Card'),
        ('Cash', 'Cash'),
    ]

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    amount_paid = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    payment_date = models.DateField()

    payment_method = models.CharField(
        max_length=50,
        choices=PAYMENT_METHODS
    )

    transaction_reference = models.CharField(
        max_length=255,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payments'
        ordering = ['-payment_date']

class BankAccount(models.Model):

    ACCOUNT_OWNER = [
        ('AIC-CIIC', 'AIC-CIIC'),
        ('Mentor', 'Mentor'),
        ('Startup', 'Startup'),
    ]

    owner_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_OWNER
    )

    startup = models.ForeignKey(
        'startups.Startup',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    bank_name = models.CharField(max_length=255)

    account_holder_name = models.CharField(max_length=255)

    account_number = models.CharField(max_length=50)

    ifsc_code = models.CharField(max_length=20)

    current_balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'bank_accounts'

class StartupBillingPlan(models.Model):

    BILLING_TYPES = [
        ('Monthly', 'Monthly'),
        ('Quarterly', 'Quarterly'),
        ('Half Yearly', 'Half Yearly'),
    ]

    startup = models.OneToOneField(
        'startups.Startup',
        on_delete=models.CASCADE,
        related_name='billing_plan'
    )

    billing_type = models.CharField(
        max_length=20,
        choices=BILLING_TYPES
    )

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'startup_billing_plans'