from typing import Any

from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView
from django.db.models import F, ExpressionWrapper, FloatField, Sum, Value, Q
from django.db.models.functions import Coalesce

from .models import Category, Product
from .utils import q_search

from reviews.models import ProductReview


class IndexView(ListView):
    template_name = 'catalog/catalog.html'
    model = Product
    context_object_name = 'cards'
    paginate_by = 3

    def get_queryset(self) -> QuerySet[Any]:
        cat_name = self.kwargs.get('cat_name')
        on_sale = self.request.GET.get('on_sale', '')
        news = self.request.GET.get('new', '')
        order_by = self.request.GET.get('order_by', 'default')
        best_sellers = self.request.GET.get('bestsellers')
        q = self.request.GET.get('q')

        filters = Q()
        if cat_name:
            filters &= Q(category__key=cat_name)

        if best_sellers:
            ids = []
            popular_products = Product.objects.annotate(
                total_sold=Coalesce(Sum(F('orderitem__quantity')), Value(0))
            ).order_by('-total_sold')[:5]
            for product in popular_products:
                ids.append(product.pk)
            filters &= Q(id__in=ids)

        products = Product.objects.all()

        if q:
            vector, search_query = q_search(q)
            products = products.annotate(
                search=vector
            ).filter(search=search_query)

        if on_sale == 'on':
            filters &= Q(discount__gt=0)

        products = products.filter(filters)

        products = products.annotate(
            total_price=ExpressionWrapper(
                F('price') * (1 - F('discount') / 100.0),
                output_field=FloatField()
            )
        )
        orders = {
            'default': 'pk',
            'price': 'total_price',
            '-price': '-total_price',
            'alphabet': 'name',
            '-alphabet': '-name',
        }
        final_ordering = [orders[order_by]]
        if news == 'on':
            if 'pk' in final_ordering:
                del final_ordering[0]
            final_ordering.append('-created_at')
            products = products.order_by(*final_ordering)[:12]
        else:
            products = products.order_by(*final_ordering)

        for product in products:
            product.total_price = int(product.total_price) if int(
                product.total_price) == product.total_price else round(product.total_price, 2)
            product.discount = int(product.discount) if int(product.discount) == product.discount else round(
                product.discount, 2)
        return products

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)
        cat_name = self.kwargs.get('cat_name')
        cat = None
        if cat_name:
            cat = get_object_or_404(Category, key=cat_name)
        context['cat_name'] = cat_name
        if cat:
            context['cat'] = cat

        params = self.request.GET.copy()
        if 'page' in params:
            params.pop('page')
        context['querystring'] = params.urlencode()
        return context


class ProductDetailsView(DetailView):
    template_name = 'catalog/product.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'product'

    def get_object(self, queryset=None) -> Model:
        product = Product.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        product.total_price = product.price * (1 - product.discount / 100)
        product.total_price = int(product.total_price) if int(product.total_price) == product.total_price else round(
            product.total_price, 2)
        product.discount = int(product.discount) if int(product.discount) == product.discount else round(
            product.discount, 2)
        product.price = int(product.price) if int(product.price) == product.price else round(product.price, 2)
        return product

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['reviews'] = ProductReview.objects.filter(product=self.get_object(), status='published')
        return context
