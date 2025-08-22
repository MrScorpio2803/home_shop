from django import forms

from .models import FeedbackMessage


class CreateMessageForm(forms.ModelForm):
    
    class Meta:
        model = FeedbackMessage
        fields = ('name', 'email', 'phone', 'topic', 'custom_topic', 'text')

    name = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField()
    topic = forms.ChoiceField()
    custom_topic = forms.CharField()
    text = forms.Textarea()



