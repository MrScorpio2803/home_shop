from django.views import View
from django.shortcuts import render
from django.db.models import F, ExpressionWrapper, FloatField

from catalog.models import Product, Category
from .models import Review

class IndexView(View):
    def get(self, req):
        new_products = Product.objects.annotate(
            total_price=ExpressionWrapper(F('price') * (1 - F('discount') / 100.0),
                                          output_field=FloatField()
                                          )
        ).order_by('-created_at')[:4]
        categories = Category.objects.all()[:3]
        for product in new_products:
            product.total_price = int(product.total_price) if int(
                product.total_price) == product.total_price else round(product.total_price, 2)

        reviews = Review.objects.all()

        # categories = [
        #     {'slug': 'sofas', 'name': 'Диваны', 'image': {'url': '/static/images/cat_sofas.jpg'}},
        #     {'slug': 'tables', 'name': 'Столы', 'image': {'url': '/static/images/cat_tables.jpg'}},
        #     {'slug': 'chairs', 'name': 'Кресла', 'image': {'url': '/static/images/cat_chairs.jpg'}},
        # ]

        # reviews = [
        #     {'author': 'Анна', 'text': 'Отличный сервис и качественная мебель! Рекомендую.'},
        #     {'author': 'Иван', 'text': 'Заказал диван, доставили вовремя и без повреждений.'},
        #     {'author': 'Мария', 'text': 'Большой выбор и приятные цены.'},
        # ]

        context = {
            'new_products': new_products,
            'categories': categories,
            'reviews': reviews,
        }

        return render(req, 'main/index.html', context=context)


class AboutContact(View):
    def get(self, req):
        return render(req, 'main/about_contact.html')


class AboutUs(View):
    def get(self, req):
        return render(req, 'main/about_us.html')


class AboutPayment(View):
    def get(self, req):
        return render(req, 'main/about_payment.html')


class AboutRefund(View):
    def get(self, req):
        return render(req, 'main/about_refund.html')
