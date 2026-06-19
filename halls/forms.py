from django import forms
from django.db.models import Q

from halls.models import Hall, HallBooking

UTILITY_CHOICES = [
    ('Chairs', 'Chairs'),
    ('Tables', 'Tables'),
    ('Water bottles', 'Water bottles'),
    ('Projector', 'Projector'),
    ('Microphone', 'Microphone'),
    ('Whiteboard', 'Whiteboard'),
    ('Wi-Fi', 'Wi-Fi'),
]


class HallBookingForm(forms.ModelForm):
    utilities = forms.MultipleChoiceField(
        choices=UTILITY_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    chairs_count = forms.IntegerField(min_value=0, required=False, initial=0)
    tables_count = forms.IntegerField(min_value=0, required=False, initial=0)
    water_bottles_count = forms.IntegerField(min_value=0, required=False, initial=0)

    class Meta:
        model = HallBooking
        fields = ['event_name', 'hall', 'booking_date', 'start_time', 'end_time', 'attendees']
        widgets = {
            'event_name': forms.TextInput(attrs={'class': 'form-control'}),
            'hall': forms.Select(attrs={'class': 'form-select'}),
            'booking_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'attendees': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def __init__(self, *args, **kwargs):
        attendees = kwargs.pop('attendees', None)
        booking_date = kwargs.pop('booking_date', None)
        start_time = kwargs.pop('start_time', None)
        end_time = kwargs.pop('end_time', None)
        super().__init__(*args, **kwargs)
        halls = Hall.objects.filter(active=True)
        if attendees:
            halls = halls.filter(capacity__gte=attendees)
        if booking_date and start_time and end_time:
            booked_ids = HallBooking.objects.filter(
                booking_date=booking_date,
                status__in=['Pending', 'Approved'],
            ).filter(
                Q(start_time__lt=end_time) & Q(end_time__gt=start_time)
            ).values_list('hall_id', flat=True)
            halls = halls.exclude(pk__in=booked_ids)
        self.fields['hall'].queryset = halls

    def save(self, commit=True):
        instance = super().save(commit=False)
        utilities = []
        for util in self.cleaned_data.get('utilities', []):
            qty = 0
            if util == 'Chairs':
                qty = self.cleaned_data.get('chairs_count') or 0
            elif util == 'Tables':
                qty = self.cleaned_data.get('tables_count') or 0
            elif util == 'Water bottles':
                qty = self.cleaned_data.get('water_bottles_count') or 0
            utilities.append({'name': util, 'quantity': qty or 1})
        instance.utilities_required = utilities
        if commit:
            instance.save()
        return instance


class AdminHallBookingForm(forms.ModelForm):
    class Meta:
        model = HallBooking
        fields = ['status']
        widgets = {'status': forms.Select(attrs={'class': 'form-select'})}
