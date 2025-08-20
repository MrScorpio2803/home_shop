from django import forms

class OrderCreateForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()
    PAYMENT_CHOICES = [
        ('0', 'Оплата картой'),
        ('1', 'Наличными/картой при получении'),
    ]
    is_payment_on_get = forms.ChoiceField(choices=PAYMENT_CHOICES)
    DELIVERY_CHOICES = [
        ('1', 'Нужна доставка'), ('0', 'Самовывоз')
    ]
    delivery = forms.ChoiceField(choices=DELIVERY_CHOICES)
    delivery_address = forms.CharField(required=False)
