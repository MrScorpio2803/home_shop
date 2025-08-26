from typing import Any

from django.views.generic import TemplateView
from django.db.models import F, ExpressionWrapper, FloatField, Sum, Value
from django.db.models.functions import Coalesce

from catalog.models import Product, Category
from reviews.models import OrderReview as Review

from feedback.forms import CreateMessageForm


class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(status='published')
        context['categories'] = Category.objects.annotate(
            total_sold=Coalesce(Sum(F('products__orderitem__quantity')), Value(0))
        ).order_by('-total_sold')[:3]

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

    def get_context_data(self):
        context = super().get_context_data()
        if self.request.user and self.request.user.is_authenticated:
            name = self.request.user.first_name if self.request.user.first_name else ''
            email = self.request.user.email if self.request.user.email else ''
        else:
            name = ''
            email = ''
        context['form'] = CreateMessageForm(initial={'name': name,
                                                     'email': email
                                                     })
        return context


class AboutUs(TemplateView):
    template_name = 'main/about_us.html'


class AboutPayment(TemplateView):
    template_name = 'main/about_payment.html'


class AboutRefund(TemplateView):
    template_name = 'main/about_refund.html'
