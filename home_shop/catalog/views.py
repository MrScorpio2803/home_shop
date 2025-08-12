from django.shortcuts import render, get_object_or_404
from django.views import View
from django.core.paginator import Paginator

from django.db.models import F, ExpressionWrapper, FloatField
from django.db.models import Q

from .models import Category, Product
from .utils import q_search, random_list_ids_for_model


class IndexView(View):

    def get(self, req, cat_name=None):
        page = req.GET.get('page', 1)

        on_sale = req.GET.get('on_sale', '')
        order_by = req.GET.get('order_by', 'default')
        best_sellers = req.GET.get('bestsellers', None)
        q = req.GET.get('q', None)
        cat = None
        filters = Q()
        if cat_name:
            filters &= Q(category__key=cat_name)
            cat = get_object_or_404(Category, key=cat_name)

        if best_sellers:
            ids = random_list_ids_for_model(Product)
            filters &= Q(id__in=ids)
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
        if best_sellers:
            paginator = Paginator(products, 4)
        else:
            paginator = Paginator(products, 3)

        cur_page = paginator.page(page)

        context = {
            'cards': cur_page,
            'cat_name': cat_name,
        }
        if cat:
            context.update({'cat': cat.name})

        return render(req, 'catalog/catalog.html', context=context)


class ProductDetailsView(View):
    def get(self, req, slug):
        product = get_object_or_404(Product, slug=slug)
        product.total_price = product.price * (1 - product.discount / 100)
        product.total_price = int(product.total_price) if int(product.total_price) == product.total_price else round(product.total_price, 2)
        product.discount = int(product.discount) if int(product.discount) == product.discount else round(product.discount, 2)
        product.price = int(product.price) if int(product.price) == product.price else round(product.price, 2)
        context = {
            'product': product
        }

        return render(req, 'catalog/product.html', context=context)
