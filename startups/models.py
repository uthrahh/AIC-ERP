import random
from django.db import models


def generate_startup_code():
    for _ in range(100):
        code = str(random.randint(1000, 9999))
        if not Startup.objects.filter(startup_code=code).exists():
            return code
    return str(random.randint(10000, 99999))


class Startup(models.Model):

    class IncubationType(models.TextChoices):
        VIRTUAL = 'virtual', 'Virtual'
        RESIDENTIAL = 'residential', 'Residential'

    class StartupStatus(models.TextChoices):
        ACTIVE = 'active', 'Active'
        GRADUATED = 'graduated', 'Graduated'
        DROPPED = 'dropped', 'Dropped'

    startup_code = models.CharField(
        max_length=10,
        unique=True,
        default=generate_startup_code
    )

    logo = models.ImageField(
        upload_to='startups/logos/',
        blank=True,
        null=True
    )

    brand_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    legal_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    company_description = models.TextField(blank=True)

    sector = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    sub_sector = models.CharField(
        max_length=100,
        blank=True
    )

    legal_status = models.CharField(
        max_length=100,
        blank=True
    )

    market_type = models.CharField(
        max_length=100,
        blank=True
    )

    trl_level = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )

    startup_readiness_level = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )

    funding_stage = models.CharField(
        max_length=100,
        blank=True
    )

    revenue_model = models.CharField(
        max_length=100,
        blank=True
    )

    startup_status = models.CharField(
        max_length=20,
        choices=StartupStatus.choices,
        default=StartupStatus.ACTIVE
    )

    operation_type = models.CharField(
        max_length=100,
        blank=True
    )

    incubation_type = models.CharField(
        max_length=20,
        choices=IncubationType.choices,
        default=IncubationType.VIRTUAL
    )

    website = models.URLField(blank=True)

    onboarding_date = models.DateField(
        null=True,
        blank=True
    )

    registration_date = models.DateField(
        null=True,
        blank=True
    )

    cin = models.CharField(
        max_length=50,
        blank=True
    )

    dpiit = models.CharField(
        max_length=50,
        blank=True
    )

    pan = models.CharField(
        max_length=20,
        blank=True
    )

    gst_number = models.CharField(
        max_length=30,
        blank=True
    )

    office_room = models.CharField(
        max_length=50,
        blank=True
    )

    office_rent = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    jobs_created = models.PositiveIntegerField(
        default=0
    )

    sales_turnover = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    startup_valuation = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    risk_level = models.PositiveSmallIntegerField(
        blank=True,
        null=True
    )

    primary_poc_name = models.CharField(
        max_length=255,
        blank=True
    )

    secondary_poc_name = models.CharField(
        max_length=255,
        blank=True
    )

    primary_poc_email = models.EmailField(
        blank=True
    )

    secondary_poc_email = models.EmailField(
        blank=True
    )

    primary_poc_phone = models.CharField(
        max_length=20,
        blank=True
    )

    secondary_poc_phone = models.CharField(
        max_length=20,
        blank=True
    )

    keywords = models.JSONField(
        default=list,
        blank=True
    )

    class Meta:
        db_table = 'startups'
        ordering = ['brand_name']

    def __str__(self):
        return self.brand_name


class Document(models.Model):
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE, related_name='documents')
    document_name = models.CharField(max_length=255)
    file = models.FileField(upload_to='startups/documents/')
    uploaded_by = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL, null=True, related_name='uploaded_documents'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'documents'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f'{self.document_name} - {self.startup.brand_name}'


class StartupTeamMember(models.Model):
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE, related_name='team_members')
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='startups/team/', blank=True, null=True)

    class Meta:
        db_table = 'startup_team_members'

    def __str__(self):
        return f'{self.name} - {self.startup.brand_name}'


class StartupMedia(models.Model):
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE, related_name='media')
    title = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='startups/media/')
    caption = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'startup_media'

    def __str__(self):
        return self.title or f'Media for {self.startup.brand_name}'

class Founder(models.Model):

    startup = models.ForeignKey(
        Startup,
        on_delete=models.CASCADE,
        related_name='founders'
    )

    founder_name = models.CharField(max_length=255)

    email = models.EmailField(
        blank=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    education = models.CharField(
        max_length=255,
        blank=True
    )

    linkedin = models.URLField(
        blank=True
    )

    is_primary_poc = models.BooleanField(
        default=False
    )

    is_secondary_poc = models.BooleanField(
        default=False
    )

    class Meta:
        db_table = 'startup_founders'

    def __str__(self):
        return f'{self.founder_name} - {self.startup.brand_name}'
    
class StartupSocialMedia(models.Model):
    PLATFORM_CHOICES = [
        ('Website', 'Website'),
        ('LinkedIn', 'LinkedIn'),
        ('Instagram', 'Instagram'),
        ('Facebook', 'Facebook'),
        ('Twitter', 'Twitter'),
        ('YouTube', 'YouTube'),
        ('Other', 'Other'),
    ]

    startup = models.ForeignKey(
        Startup,
        on_delete=models.CASCADE,
        related_name='social_links'
    )

    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)

    url = models.URLField()

    class Meta:
        db_table = 'startup_social_media'


class StartupFunding(models.Model):
    FUNDING_TYPES = [
        ('Government Grant', 'Government Grant'),
        ('Seed Fund', 'Seed Fund'),
        ('Angel Investment', 'Angel Investment'),
        ('VC Investment', 'VC Investment'),
        ('CSR Grant', 'CSR Grant'),
        ('Debt Funding', 'Debt Funding'),
        ('Other', 'Other'),
    ]

    startup = models.ForeignKey(
        Startup,
        on_delete=models.CASCADE,
        related_name='funding_records'
    )

    funding_type = models.CharField(max_length=100, choices=FUNDING_TYPES)

    investor = models.CharField(max_length=255, blank=True)

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    funding_date = models.DateField(
        null=True,
        blank=True
    )

    remarks = models.TextField(blank=True)

    class Meta:
        db_table = 'startup_funding'


class StartupLoan(models.Model):

    startup = models.ForeignKey(
        Startup,
        on_delete=models.CASCADE,
        related_name='loans'
    )

    lender = models.CharField(max_length=255)

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    outstanding_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    interest_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    loan_date = models.DateField(
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'startup_loans'


class StartupAward(models.Model):

    startup = models.ForeignKey(
        Startup,
        on_delete=models.CASCADE,
        related_name='awards'
    )

    award_name = models.CharField(max_length=255)

    organization = models.CharField(max_length=255)

    award_date = models.DateField(
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'startup_awards'


class StartupIPR(models.Model):

    IPR_TYPES = [
        ('Patent', 'Patent'),
        ('Trademark', 'Trademark'),
        ('Copyright', 'Copyright'),
        ('Design Right', 'Design Right'),
        ('Trade Secret', 'Trade Secret'),
    ]

    startup = models.ForeignKey(
        Startup,
        on_delete=models.CASCADE,
        related_name='iprs'
    )

    ipr_type = models.CharField(max_length=50, choices=IPR_TYPES)

    title = models.CharField(max_length=255)

    application_number = models.CharField(
        max_length=100,
        blank=True
    )

    filing_date = models.DateField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=100,
        blank=True
    )

    class Meta:
        db_table = 'startup_ipr'


class StartupFinancial(models.Model):

    startup = models.ForeignKey(
        Startup,
        on_delete=models.CASCADE,
        related_name='financials'
    )

    quarter = models.CharField(max_length=20)

    revenue = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    expenses = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    profit = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    valuation = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    jobs_created = models.PositiveIntegerField(default=0)

    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'startup_financials'


class StartupBankAccount(models.Model):

    startup = models.ForeignKey(
        Startup,
        on_delete=models.CASCADE,
        related_name='bank_accounts'
    )

    bank_name = models.CharField(max_length=255)

    ifsc = models.CharField(max_length=20)

    account_number = models.CharField(max_length=50)

    account_holder = models.CharField(max_length=255)

    current_balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    class Meta:
        db_table = 'startup_bank_accounts'
    
class StartupEmployee(models.Model):

    startup = models.ForeignKey(
        Startup,
        on_delete=models.CASCADE,
        related_name='employees'
    )

    employee_name = models.CharField(max_length=255)

    designation = models.CharField(max_length=255)

    compensation = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    joining_date = models.DateField(
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'startup_employees'

class QuarterlyFinancialUpdate(models.Model):

    startup = models.ForeignKey(
        Startup,
        on_delete=models.CASCADE,
        related_name='quarterly_updates'
    )

    quarter = models.CharField(max_length=20)

    financial_year = models.CharField(max_length=20)

    revenue = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    expenses = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    profit = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    valuation = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    jobs_created = models.PositiveIntegerField(default=0)

    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'quarterly_financial_updates'


class ReminderTracker(models.Model):

    REMINDER_TYPES = [
        ('Quarterly Update', 'Quarterly Update'),
        ('Invoice Payment', 'Invoice Payment'),
        ('Profile Update', 'Profile Update'),
    ]

    startup = models.ForeignKey(
        Startup,
        on_delete=models.CASCADE
    )

    reminder_type = models.CharField(
        max_length=100,
        choices=REMINDER_TYPES
    )

    due_date = models.DateField()

    reminder_sent = models.BooleanField(default=False)

    sent_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'reminder_tracker'

