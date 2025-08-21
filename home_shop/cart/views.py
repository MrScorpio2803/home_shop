from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.template.loader import render_to_string

from .models import Cart
from .mixins import CartMixin
from .utils import get_user_carts

from catalog.models import Product

class CartAddView(CartMixin, View):
    def post(self, req):
        product_id = req.POST.get('product_id')
        product = Product.objects.get(id=product_id)

        cart = self.get_cart(req, product=product)
        if cart:
            cart.quantity += 1
            cart.save()
        else:
            Cart.objects.create(user=req.user if req.user.is_authenticated else None, 
                                session_key=req.session.session_key if not req.user.is_authenticated else None,
                                product=product, quantity=1)

        response_data = {
            'message': 'Товар успешно добавлен в корзину',
            'cart_items_html': self.render_cart(req)
        }
        return JsonResponse(response_data)


class CartChangeView(CartMixin, View):
    def post(self, req):
        cart_id = req.POST.get('cart_id')
        quantity = req.POST.get('quantity')

        cart = self.get_cart(req, cart_id=cart_id)
        cart.quantity = quantity
        cart.save()

        quantity = cart.quantity

        response_data = {
            'message': 'Товар успешно добавлен в корзину',
            'cart_items_html': self.render_cart(req),
            'quantity': quantity
        }
        return JsonResponse(response_data)


class CartRemoveView(CartMixin, View):
    def post(self, req):
        cart_id = req.POST.get('cart_id')

        cart = self.get_cart(req, cart_id=cart_id)
        quantity = cart.quantity
        cart.delete()

        response_data = {
            'message': 'Товар успешно добавлен в корзину',
            'cart_items_html': self.render_cart(req),
            'quantity_deleted': quantity
        }
        return JsonResponse(response_data)
