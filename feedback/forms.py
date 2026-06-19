from django import forms
from feedback.models import Complaint, GeneralFeedback


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['subject', 'description']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class GeneralFeedbackForm(forms.ModelForm):
    class Meta:
        model = GeneralFeedback
        fields = ['feedback_type', 'rating', 'comments']
        widgets = {
            'feedback_type': forms.Select(attrs={'class': 'form-select'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class AdminComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['status']
        widgets = {'status': forms.Select(attrs={'class': 'form-select'})}
