from django.urls import path

from .views import CreateFeedbackMessageView

app_name = 'feedback'

urlpatterns = [
    path('create-message/', CreateFeedbackMessageView.as_view(), name='create_message'),
]