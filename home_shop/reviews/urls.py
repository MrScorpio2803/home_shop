from django.urls import path

from .views import CreateOrderReviewView, EditOrderReviewView, CreateProductReviewView, EditProductReviewView

app_name = 'reviews'

urlpatterns = [
    path('create-order-review/<int:order_id>', CreateOrderReviewView.as_view(), name='create_order_review'),
    path('edit-order-review/<int:order_id>', EditOrderReviewView.as_view(), name='edit_order_review'),
    path('create-product-review/<slug:product_slug>', CreateProductReviewView.as_view(), name='create_product_review'),
    path('edit-product-review/<slug:product_slug>', EditProductReviewView.as_view(), name='edit_product_review'),
]
