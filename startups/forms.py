from django import forms
from startups.models import Startup, Document, StartupTeamMember, StartupMedia
from startups.models import (
    Founder,
    StartupFunding,
    StartupLoan,
    StartupAward,
    StartupIPR,
    StartupEmployee,
    StartupBankAccount,
    QuarterlyFinancialUpdate,
)

class StartupProfileForm(forms.ModelForm):
    class Meta:
        model = Startup

        fields = [
            'logo',
            'brand_name',
            'legal_name',
            'company_description',
            'sector',
            'sub_sector',
            'legal_status',
            'market_type',
            'trl_level',
            'startup_readiness_level',
            'funding_stage',
            'revenue_model',
            'operation_type',
            'incubation_type',
            'website',
            'onboarding_date',
            'registration_date',
            'cin',
            'dpiit',
            'pan',
            'gst_number',
            'office_room',
        ]

        widgets = {
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'legal_name': forms.TextInput(attrs={'class': 'form-control'}),
            'company_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'sector': forms.TextInput(attrs={'class': 'form-control'}),
            'sub_sector': forms.TextInput(attrs={'class': 'form-control'}),
            'legal_status': forms.TextInput(attrs={'class': 'form-control'}),
            'market_type': forms.TextInput(attrs={'class': 'form-control'}),
            'trl_level': forms.NumberInput(attrs={'class': 'form-control'}),
            'startup_readiness_level': forms.NumberInput(attrs={'class': 'form-control'}),
            'funding_stage': forms.TextInput(attrs={'class': 'form-control'}),
            'revenue_model': forms.TextInput(attrs={'class': 'form-control'}),
            'operation_type': forms.TextInput(attrs={'class': 'form-control'}),
            'incubation_type': forms.Select(attrs={'class': 'form-select'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'onboarding_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'registration_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cin': forms.TextInput(attrs={'class': 'form-control'}),
            'dpiit': forms.TextInput(attrs={'class': 'form-control'}),
            'pan': forms.TextInput(attrs={'class': 'form-control'}),
            'gst_number': forms.TextInput(attrs={'class': 'form-control'}),
            'office_room': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AdminStartupForm(forms.ModelForm):
    class Meta:
        model = Startup

        fields = [
            'logo',
            'brand_name',
            'legal_name',
            'company_description',
            'sector',
            'startup_status',
            'funding_stage',
            'startup_valuation',
            'jobs_created',
        ]

        widgets = {
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control'}),
            'legal_name': forms.TextInput(attrs={'class': 'form-control'}),
            'company_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'sector': forms.TextInput(attrs={'class': 'form-control'}),
            'startup_status': forms.Select(attrs={'class': 'form-select'}),
            'funding_stage': forms.TextInput(attrs={'class': 'form-control'}),
            'startup_valuation': forms.NumberInput(attrs={'class': 'form-control'}),
            'jobs_created': forms.NumberInput(attrs={'class': 'form-control'}),
        }


# class AdminStartupForm(forms.ModelForm):
#     class Meta:
#         model = Startup
#         fields = [
#             'company_name', 'type', 'description', 'tagline', 'domain',
#             'address', 'email', 'phone', 'logo', 'status', 'funding_total',
#             'valuation', 'incubation_year', 'profile_complete',
#         ]
#         widgets = {f: forms.TextInput(attrs={'class': 'form-control'}) for f in [
#             'company_name', 'tagline', 'domain', 'email', 'phone', 'incubation_year'
#         ]}
#         widgets.update({
#             'type': forms.Select(attrs={'class': 'form-select'}),
#             'status': forms.Select(attrs={'class': 'form-select'}),
#             'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
#             'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
#             'logo': forms.FileInput(attrs={'class': 'form-control'}),
#             'funding_total': forms.NumberInput(attrs={'class': 'form-control'}),
#             'valuation': forms.NumberInput(attrs={'class': 'form-control'}),
#             'profile_complete': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
#         })


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['document_name', 'file']
        widgets = {
            'document_name': forms.TextInput(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }


class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = StartupTeamMember
        fields = ['name', 'role', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }


class StartupMediaForm(forms.ModelForm):
    class Meta:
        model = StartupMedia
        fields = ['title', 'image', 'caption']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'caption': forms.TextInput(attrs={'class': 'form-control'}),
        }

class FounderForm(forms.ModelForm):
    class Meta:
        model = Founder
        exclude = ['startup']


class FundingForm(forms.ModelForm):
    class Meta:
        model = StartupFunding
        exclude = ['startup']


class LoanForm(forms.ModelForm):
    class Meta:
        model = StartupLoan
        exclude = ['startup']


class AwardForm(forms.ModelForm):
    class Meta:
        model = StartupAward
        exclude = ['startup']


class IPRForm(forms.ModelForm):
    class Meta:
        model = StartupIPR
        exclude = ['startup']


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = StartupEmployee
        exclude = ['startup']


class BankAccountForm(forms.ModelForm):
    class Meta:
        model = StartupBankAccount
        exclude = ['startup']


class QuarterlyUpdateForm(forms.ModelForm):
    class Meta:
        model = QuarterlyFinancialUpdate
        exclude = ['startup']