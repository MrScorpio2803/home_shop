from django import forms

from .models import OrderReview, ProductReview


class OrderReviewDetailForm(forms.ModelForm):
    class Meta:
        model = OrderReview
        fields = ('rating', 'text')
    rating = forms.IntegerField()
    text = forms.Textarea()


class ProductReviewDetailForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ('rating', 'text')
    rating = forms.IntegerField()
    text = forms.Textarea()
