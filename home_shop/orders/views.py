from django.forms import ValidationError
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.db import transaction
from django.contrib import messages

from .forms import OrderCreateForm

from cart.models import Cart
from .models import Order, OrderItem

class CreateOrderView(LoginRequiredMixin, View):
    login_url = reverse_lazy('users:login')

    def get(self, req):
        initials = {
            'first_name': req.user.first_name,
            'last_name': req.user.last_name
        }
        if req.user.phone:
            phone = req.user.phone
            initials['phone_number'] = phone
        form = OrderCreateForm(initial=initials)
        return render(req, 'orders/create_order.html', context={'form': form})

    def post(self, req):
        form = OrderCreateForm(data=req.POST)
        if form.is_valid():
            print('V IF')
            try:
                with transaction.atomic():
                    user = req.user
                    carts = Cart.objects.filter(user=user)
                    if carts.exists():
                        order = Order.objects.create(
                            user=user,
                            phone_number = form.cleaned_data['phone_number'],
                            delivery = form.cleaned_data['delivery'],
                            delivery_address = form.cleaned_data['delivery_address'],
                            is_payment_on_get = form.cleaned_data['is_payment_on_get']
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

                        messages.success(req, "Ваш заказ успешно оформлен! Мы свяжемся с вами.")
                        return redirect('users:profile')
            except ValidationError as e:
                print(f'Выявлено исключение: {e}')
                messages.success(req, str(e))
                return redirect('users:cart')
            return redirect('users:profile')
        return render(req, 'orders/create_order.html', context={'form': form})

