from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView

from .views import UserLoginView, RegisterView, ProfileView, CartView


app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('registration/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('main:index')), name='logout'),
    path('cart/', CartView.as_view(), name='cart'),
]
