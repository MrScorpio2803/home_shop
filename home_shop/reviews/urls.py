from django.urls import path

from .views import CreateReviewView

app_name = 'reviews'

urlpatterns = [
    path('create-review/', CreateReviewView.as_view(), name='create_review'),
]