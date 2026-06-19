from django import forms
from django.core.exceptions import ValidationError
from applications.models import Application, ApplicationReview, SERVICE_CHOICES
import re

REFERENCE_CHOICES = [
('Social Media', 'Social Media'),
('Website', 'Website'),
('Friend', 'Friend'),
('Faculty', 'Faculty'),
('Startup Event', 'Startup Event'),
('Incubated Startup', 'Incubated Startup'),
('Newspaper', 'Newspaper'),
('Other', 'Other'),
]

class ApplicationForm(forms.ModelForm):

    services_required = forms.MultipleChoiceField(
        choices=SERVICE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    other_service = forms.CharField(
        required=False,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Specify other service'
            }
        )
    )

    reference_source = forms.ChoiceField(
        choices=REFERENCE_CHOICES,
        widget=forms.Select(
            attrs={'class': 'form-select'}
        )
    )

    class Meta:
        model = Application

        fields = [
            'founder_name',
            'startup_name',
            'building_name',
            'street',
            'pincode',
            'area',
            'city',
            'state',
            'contact_number',
            'email',
            'problem_statement',
            'solution',
            'services_required',
            'other_service',
            'reference_source',
        ]

        widgets = {
            'founder_name': forms.TextInput(attrs={'class': 'form-control'}),
            'startup_name': forms.TextInput(attrs={'class': 'form-control'}),

            'building_name': forms.TextInput(attrs={'class': 'form-control'}),

            'street': forms.TextInput(attrs={'class': 'form-control'}),

            'pincode': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'maxlength': 6
                }
            ),

            'area': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'readonly': True
                }
            ),

            'city': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'readonly': True
                }
            ),

            'state': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'readonly': True
                }
            ),

            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),

            'email': forms.EmailInput(attrs={'class': 'form-control'}),

            'problem_statement': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'maxlength': 500,
                    'placeholder': 'Explain the problem identified in maximum 500 characters'
                }
            ),

            'solution': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'maxlength': 500,
                    'placeholder': 'Explain your proposed solution in maximum 500 characters'
                }
            ),
        }

    def clean_startup_name(self):
        value = self.cleaned_data['startup_name']

        if not re.match(r'^[A-Za-z0-9 ]+$', value):
            raise ValidationError(
                'Startup name can contain only alphabets, digits and spaces.'
            )

        return value

    def clean_founder_name(self):
        value = self.cleaned_data['founder_name']

        if not re.match(r'^[A-Za-z ]+$', value):
            raise ValidationError(
                'Founder name can contain only alphabets and spaces.'
            )

        return value

    def clean_contact_number(self):
        value = self.cleaned_data['contact_number']

        if not re.match(r'^[0-9]{10}$', value):
            raise ValidationError(
                'Contact number must be exactly 10 digits.'
            )

        return value

    def clean_pincode(self):
        value = self.cleaned_data['pincode']

        if not re.match(r'^[0-9]{6}$', value):
            raise ValidationError(
                'Pincode must be exactly 6 digits.'
            )

        import requests

        try:
            response = requests.get(
                f'https://api.postalpincode.in/pincode/{value}',
                timeout=5
            )

            data = response.json()

            if (
                data[0]['Status'] != 'Success'
                or not data[0]['PostOffice']
            ):
                raise ValidationError(
                    'Please enter a valid Indian pincode.'
                )

        except Exception:
            raise ValidationError(
                'Invalid pincode.'
            )

        return value

    def clean_building_name(self):
        value = self.cleaned_data['building_name']

        if not re.match(r'^[A-Za-z0-9/ ]+$', value):
            raise ValidationError(
                'Building name can contain only alphabets, digits and slash (/).'
            )

        return value

    def clean_street(self):
        value = self.cleaned_data['street']

        if not re.match(r'^[A-Za-z0-9 ]+$', value):
            raise ValidationError(
                'Street can contain only alphabets, digits and spaces.'
            )

        return value

    def clean_other_service(self):
        value = self.cleaned_data.get('other_service')

        if value and not re.match(r'^[A-Za-z0-9, ]+$', value):
            raise ValidationError(
                'Only alphabets, digits, commas and spaces allowed.'
            )

        return value

class ApplicationReviewForm(forms.ModelForm):

    status = forms.ChoiceField(
        choices=Application.Status.choices,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    class Meta:
        model = ApplicationReview

        fields = [
            'innovation_score',
            'commercialization_score',
            'feasibility_score',
            'comments',
            'hod_name',
            'department',
        ]

        widgets = {
            'innovation_score': forms.NumberInput(
                attrs={'class': 'form-control', 'min': 1, 'max': 10}
            ),
            'commercialization_score': forms.NumberInput(
                attrs={'class': 'form-control', 'min': 1, 'max': 10}
            ),
            'feasibility_score': forms.NumberInput(
                attrs={'class': 'form-control', 'min': 1, 'max': 10}
            ),
            'comments': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4}
            ),
            'hod_name': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'department': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
        }