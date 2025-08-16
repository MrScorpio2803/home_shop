from django.urls import path

from .views import CartAddView, CartChangeView, CartRemoveView


app_name = 'cart'

urlpatterns = [
    path('cart-add/', CartAddView.as_view(), name='cart_add'),
    path('cart-change/', CartChangeView.as_view(), name='cart_change'),
    path('cart-remove/', CartRemoveView.as_view(), name='cart_remove'),

]
