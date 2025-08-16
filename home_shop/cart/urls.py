from django.urls import path

from .views import cart_add, CartChangeView, cart_remove


app_name = 'cart'

urlpatterns = [
    path('cart-add/<slug:product_slug>', cart_add, name='cart_add'),
    path('cart-change/<slug:product_slug>', CartChangeView.as_view(), name='cart_change'),
    path('cart-remove/<int:cart_id>', cart_remove, name='cart_remove'),

]
