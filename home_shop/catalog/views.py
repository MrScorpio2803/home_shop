from django.shortcuts import render, get_object_or_404
from django.views import View
from django.core.paginator import Paginator

from django.db.models import F, ExpressionWrapper, FloatField
from django.db.models import Q

from .models import Category, Product
from .utils import q_search


class IndexView(View):

    def get(self, req, cat_name=None):
        page = req.GET.get('page', 1)

        on_sale = req.GET.get('on_sale', '')
        order_by = req.GET.get('order_by', 'default')

        q = req.GET.get('q', None)


        filters = Q()
        if cat_name:
            filters &= Q(category__key=cat_name)
        if q:
            filters &= q_search(q)
        if on_sale == 'on':
            filters &= Q(discount__gt=0)
        products = Product.objects.annotate(
            total_price=ExpressionWrapper(F('price') * (1 - F('discount') / 100.0),
                                          output_field=FloatField()
                                          )
        ).filter(filters)

        if order_by == 'default':
            products = products.order_by('pk')
        elif order_by == 'price':
            products = products.order_by('total_price')
        elif order_by == '-price':
            products = products.order_by('-total_price')
        elif order_by == 'alphabet':
            products = products.order_by('name')
        elif order_by == '-alphabet':
            products = products.order_by('-name')
        for product in products:
            product.total_price = int(product.total_price) if int(
                product.total_price) == product.total_price else round(product.total_price, 2)
            product.discount = int(product.discount) if int(product.discount) == product.discount else round(
                product.discount, 2)
        paginator = Paginator(products, 3)
        cur_page = paginator.page(page)

        context = {
            'cards': cur_page,
        }
        return render(req, 'catalog/catalog.html', context=context)
# Create your views here.
