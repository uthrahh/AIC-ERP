from django import forms

from mentors.models import Mentor
from mentorship.models import MentorshipBooking


class MentorshipBookingForm(forms.ModelForm):
    class Meta:
        model = MentorshipBooking
        fields = ['mentor', 'session_date', 'start_time', 'end_time', 'notes']
        widgets = {
            'mentor': forms.Select(attrs={'class': 'form-select'}),
            'session_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mentor'].queryset = Mentor.objects.filter(is_active=True)


class AdminMentorshipForm(forms.ModelForm):
    class Meta:
        model = MentorshipBooking
        fields = ['status', 'bill_amount']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'bill_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
