from django.urls import path, include
from .views import IndexView, ProductDetailsView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'catalog'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('search/', IndexView.as_view(), name='search'),
    path('product/<str:slug>/', ProductDetailsView.as_view(), name='product'),
    path('<str:cat_name>/', IndexView.as_view(), name='catergory_products'),

]


