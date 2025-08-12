from django.urls import path

from .views import LoginView, RegisterView, profile_view, logout_view


app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegisterView.as_view(), name='register'),
    path('profile/', profile_view, name='profile'),
    path('logout/', logout_view, name='logout'),
]
