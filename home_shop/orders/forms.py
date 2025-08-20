import re

from django import forms


class OrderCreateForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()
    PAYMENT_CHOICES = [
        ('0', 'False'),
        ('1', 'True'),
    ]
    is_payment_on_get = forms.ChoiceField(choices=PAYMENT_CHOICES)
    DELIVERY_CHOICES = [
        ('1', 'True'), ('0', 'False')
    ]
    delivery = forms.ChoiceField(choices=DELIVERY_CHOICES)
    delivery_address = forms.CharField(required=False)

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']

        if not data.isdigit():
            raise forms.ValidationError('Номер телефона должен состоять только из цифр')

        pattern = re.compile(r'^\d{10}$')
        if not pattern.match(data):
            raise forms.ValidationError('Неверный формат номера')

        return data
