from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.views import View
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib import messages

from .forms import OrderReviewCreateForm

from orders.models import Order


class CreateReviewView(View):

    def get(self, req, order_id):
        form = OrderReviewCreateForm()
        order = Order.objects.get(pk=order_id)

        return render(req, 'reviews/create_order_review.html', {'form': form, 'order': order})

    def post(self, req, order_id):
        form = OrderReviewCreateForm(data=req.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.order = Order.objects.get(pk=order_id)
            form.user = req.user
            form.save()

            return redirect('users:profile')
