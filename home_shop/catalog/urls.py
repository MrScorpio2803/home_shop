from django.urls import path, include
from .views import IndexView
from django.conf import settings
from django.conf.urls.static import static

app_name = 'catalog'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('search/', IndexView.as_view(), name='search'),
    path('<str:cat_name>/', IndexView.as_view(), name='catergory_products'),
    
    # path('about/', AboutUs.as_view(), name='about_us'),
    # path('contact/', AboutContact.as_view(), name='about_contact'),
    # path('payment/', AboutPayment.as_view(), name='about_payment'),
    # path('refund/', AboutRefund.as_view(), name='about_refund'),
]


