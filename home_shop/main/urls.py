from django.urls import path

from .views import IndexView, AboutContact, AboutUs, AboutPayment, AboutRefund

app_name = 'main'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about/', AboutUs.as_view(), name='about_us'),
    path('contact/', AboutContact.as_view(), name='about_contact'),
    path('payment/', AboutPayment.as_view(), name='about_payment'),
    path('refund/', AboutRefund.as_view(), name='about_refund'),
]
