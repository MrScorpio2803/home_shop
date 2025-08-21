from typing import Any

from django.views.generic import TemplateView
from django.db.models import F, ExpressionWrapper, FloatField

from catalog.models import Product, Category
from .models import Review


class IndexView(TemplateView):
    template_name = 'main/index.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.all()
        context['categories'] = Category.objects.all()[:3]
        
        new_products = Product.objects.annotate(
            total_price=ExpressionWrapper(F('price') * (1 - F('discount') / 100.0),
                                          output_field=FloatField()
                                          )
        ).order_by('-created_at')[:4]
        
        for product in new_products:
            product.total_price = int(product.total_price) if int(
                product.total_price) == product.total_price else round(product.total_price, 2)
        context['new_products'] = new_products

        return context


class AboutContact(TemplateView):
    template_name = 'main/about_contact.html'


class AboutUs(TemplateView):
    template_name = 'main/about_us.html'


class AboutPayment(TemplateView):
    template_name = 'main/about_payment.html'


class AboutRefund(TemplateView):  
    template_name = 'main/about_refund.html'
