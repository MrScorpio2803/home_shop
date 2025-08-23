from django import forms

from .models import FeedbackMessage


class CreateMessageForm(forms.ModelForm):

    class Meta:
        model = FeedbackMessage
        fields = ('name', 'email', 'topic', 'custom_topic', 'text')

    TOPIC_CHOICES = [
        ('order', 'Вопрос по заказу'),
        ('product', 'Вопрос по товару'),
        ('complaint', 'Жалоба'),
        ('suggestion', 'Предложение'),
        ('other', 'Другое'),
    ]

    name = forms.CharField()
    email = forms.EmailField()
    topic = forms.ChoiceField(choices=TOPIC_CHOICES)
    custom_topic = forms.CharField(required=False)
    text = forms.Textarea()



