from django import forms
from labs.models import LabBooking, Lab, Equipment


class LabBookingForm(forms.ModelForm):
    equipment = forms.ModelMultipleChoiceField(
        queryset=Equipment.objects.filter(availability_status='available'),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = LabBooking
        fields = ['lab', 'requested_date', 'start_time', 'end_time']
        widgets = {
            'lab': forms.Select(attrs={'class': 'form-select'}),
            'requested_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        lab_id = self.data.get('lab') or (self.instance.lab_id if self.instance.pk else None)
        if lab_id:
            self.fields['equipment'].queryset = Equipment.objects.filter(
                lab_id=lab_id, availability_status='available'
            )


class AdminLabBookingForm(forms.ModelForm):
    class Meta:
        model = LabBooking
        fields = ['status']
        widgets = {'status': forms.Select(attrs={'class': 'form-select'})}
