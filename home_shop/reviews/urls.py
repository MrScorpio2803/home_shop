from django.urls import path

from .views import CreateReviewView

app_name = 'reviews'

urlpatterns = [
    path('create-review/<int:order_id>', CreateReviewView.as_view(), name='create_order_review'),
]
