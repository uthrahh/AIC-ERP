from django import forms
from finance.models import Invoice, Payment


class InvoiceForm(forms.ModelForm):

    class Meta:
        model = Invoice

        fields = [
            'startup',
            'invoice_number',
            'invoice_type',
            'amount',
            'issued_date',
            'due_date',
            'status',
            'remarks',
        ]

        widgets = {
            'startup': forms.Select(attrs={'class': 'form-select'}),

            'invoice_number': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'invoice_type': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'amount': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.01'}
            ),

            'issued_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),

            'due_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),

            'status': forms.Select(
                attrs={'class': 'form-select'}
            ),

            'remarks': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3
                }
            ),
        }


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment

        fields = [
            'amount_paid',
            'payment_date',
            'payment_method',
            'transaction_reference',
        ]

        widgets = {
            'amount_paid': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'step': '0.01'
                }
            ),

            'payment_date': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),

            'payment_method': forms.Select(
                attrs={'class': 'form-select'}
            ),

            'transaction_reference': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
        }