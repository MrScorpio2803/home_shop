from django.urls import path

from .views import cart_add, CartChangeView, CartRemoveView


app_name = 'cart'

urlpatterns = [
    path('cart-add/<slug:product_slug>', cart_add, name='cart_add'),
    path('cart-change/<slug:product_slug>', CartChangeView.as_view(), name='cart_change'),
    path('cart-remove/<slug:product_slug>', CartRemoveView.as_view(), name='cart_remove'),

]
