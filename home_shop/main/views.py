from django.views import View
from django.shortcuts import render


class IndexView(View):
    def get(self, req):

        new_products = [
            {'id': 1, 'name': 'Диван Лорд', 'price': 35000, 'image': {'url': '/static/images/sofa_lord.jpg'}},
            {'id': 2, 'name': 'Стол Паркет', 'price': 15000, 'image': {'url': '/static/images/table_parket.jpg'}},
            {'id': 3, 'name': 'Кресло Уют', 'price': 12000, 'image': {'url': '/static/images/chair_cozy.jpg'}},
            {'id': 4, 'name': 'Шкаф Классика', 'price': 27000, 'image': {'url': '/static/images/wardrobe_classic.jpg'}},
        ]

        categories = [
            {'slug': 'sofas', 'name': 'Диваны', 'image': {'url': '/static/images/cat_sofas.jpg'}},
            {'slug': 'tables', 'name': 'Столы', 'image': {'url': '/static/images/cat_tables.jpg'}},
            {'slug': 'chairs', 'name': 'Кресла', 'image': {'url': '/static/images/cat_chairs.jpg'}},
        ]

        reviews = [
            {'author': 'Анна', 'text': 'Отличный сервис и качественная мебель! Рекомендую.'},
            {'author': 'Иван', 'text': 'Заказал диван, доставили вовремя и без повреждений.'},
            {'author': 'Мария', 'text': 'Большой выбор и приятные цены.'},
        ]

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
