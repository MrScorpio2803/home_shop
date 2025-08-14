from django.urls import path

from .views import CartAddView, CartChangeView, CartRemoveView


app_name = 'cart'

urlpatterns = [
    path('cart-add/<slug:product_slug>', CartAddView, name='cart_add'),
    path('cart-change/<slug:product_slug>', CartChangeView, name='cart_change'),
    path('cart-remove/<slug:product_slug>', CartRemoveView, name='cart_remove'),

]
