from typing import Any
from django.db.models.base import Model as Model
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, TemplateView
from django.views import View
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib import messages

from .models import OrderReview

from .forms import OrderReviewDetailForm, ProductReviewDetailForm

from .models import ProductReview
from orders.models import Order, OrderItem
from catalog.models import Product


class CreateOrderReviewView(CreateView):
    template_name = 'reviews/order_review.html'
    form_class = OrderReviewDetailForm
    model = OrderReview
    success_url = reverse_lazy('users:profile')

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        self.order = get_object_or_404(Order, pk=kwargs['order_id'])

        if OrderReview.objects.filter(order=self.order).exists():
            messages.error(request, 'На этот заказ уже добавлен отзыв')
            return redirect('users:profile')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.user = self.request.user
        form.instance.order = self.order

        messages.success(
            self.request,
            'Спасибо за ваш отзыв! Он будет опубликован после проверки модератором.'
        )

        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['order'] = self.order

        return context


class EditOrderReviewView(UpdateView):
    template_name = 'reviews/order_review.html'
    form_class = OrderReviewDetailForm
    model = OrderReview
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None) -> Model:
        review = get_object_or_404(OrderReview, order_id=self.kwargs['order_id'])
        return review

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.get(pk=self.kwargs['order_id'])

        return context


class CreateProductReviewView(View):
    def post(self, req, product_slug):
        form = ProductReviewDetailForm(data=req.POST)
        product = get_object_or_404(Product, slug=product_slug)
        if form.is_valid():
            if ProductReview.objects.filter(
                    product=product,
                    user=self.request.user
            ).exists():
                messages.warning(req, 'Вы уже оставляли отзыв на этот товар!')
                return redirect(reverse('catalog:product', kwargs={'slug': product_slug}))

            form.instance.product = product
            form.instance.user = self.request.user
            form.save()
            messages.success(req, 'Ваш отзыв успешно отправлен на модерацию!')
        else:
            print(form.errors)
        return redirect('catalog:catalog')


class EditProductReviewView(View):
    def post(self, req, product_slug):
        review = ProductReview.objects.get(product__slug=product_slug, user=req.user)
        form = ProductReviewDetailForm(data=req.POST)
        if form.is_valid():
            data = form.cleaned_data
            review.text = data['text']
            review.rating = data['rating']
            review.save()
            messages.success(req, 'Ваш отзыв успешно отправлен на модерацию!')
        else:
            print(form.errors)
        return redirect('catalog:product')


class ListReviewsView(TemplateView):
    template_name = 'reviews/list_user_reviews.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = OrderReview.objects.filter(user=self.request.user)
        products = ProductReview.objects.filter(user=self.request.user)

        context['total_count'] = orders.count() + products.count()
