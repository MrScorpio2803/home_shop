from typing import Any
from django.forms import ValidationError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.db import transaction
from django.contrib import messages

from .forms import OrderCreateForm

from cart.models import Cart
from .models import Order, OrderItem


class CreateOrderView(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('users:login')
    template_name = 'orders/create_order.html'
    form_class = OrderCreateForm
    success_url = reverse_lazy('users:profile')

    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        phone = self.request.user.phone
        if phone:
            initial['phone_number'] = phone[1:]
        return initial

    def form_valid(self, form: Any) -> HttpResponse:
        try:
            with transaction.atomic():
                user = self.request.user
                carts = Cart.objects.filter(user=user)
                if carts.exists():
                    order = Order.objects.create(
                        user=user,
                        phone_number=form.cleaned_data['phone_number'],
                        delivery=form.cleaned_data['delivery'],
                        delivery_address=form.cleaned_data['delivery_address'],
                        is_payment_on_get=form.cleaned_data['is_payment_on_get']
                    )
                    for cart in carts:
                        product = cart.product
                        print(product)

                        name = cart.product.name
                        price = cart.product.get_total_price()
                        quantity = cart.quantity

                        if product.quantity < quantity:
                            raise ValidationError(f'Недостаточное количество товара {name} на складе.\
                                                    В наличии: {product.quantity}')
                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            name=name,
                            price=price,
                            quantity=quantity
                        )
                        product.quantity -= quantity
                        product.save()
                    carts.delete()

                    messages.success(self.request, "Ваш заказ успешно оформлен! Мы свяжемся с вами.")
                    return redirect('users:profile')
        except ValidationError as e:
            print(f'Выявлено исключение: {e}')
            messages.success(self.request, str(e))
            return redirect('users:cart')
        return super().form_valid(form)

    # def get(self, req):
    #     initials = {
    #         'first_name': req.user.first_name,
    #         'last_name': req.user.last_name
    #     }
    #     if req.user.phone:
    #         phone = req.user.phone
    #         initials['phone_number'] = phone
    #     form = OrderCreateForm(initial=initials)
    #     return render(req, 'orders/create_order.html', context={'form': form})

    # def post(self, req):
    #     form = OrderCreateForm(data=req.POST)
    #     if form.is_valid():

    #         return redirect('users:profile')
    #     return render(req, 'orders/create_order.html', context={'form': form})
