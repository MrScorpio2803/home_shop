from django import forms

from .models import OrderReview


class OrderReviewDetailForm(forms.ModelForm):
    class Meta:
        model = OrderReview
        fields = ('rating', 'text')
    rating = forms.IntegerField()
    text = forms.Textarea()
