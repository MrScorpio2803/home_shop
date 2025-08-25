from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.contrib import messages

from .models import OrderReview

from .forms import OrderReviewDetailForm

from orders.models import Order


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
