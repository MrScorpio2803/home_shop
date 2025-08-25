from django.urls import path

from .views import CreateOrderReviewView, EditOrderReviewView

app_name = 'reviews'

urlpatterns = [
    path('create-review/<int:order_id>', CreateOrderReviewView.as_view(), name='create_order_review'),
    path('edit-review/<int:order_id>', EditOrderReviewView.as_view(), name='edit_order_review')
]
