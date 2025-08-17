from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.template.loader import render_to_string

from .models import Cart
from catalog.models import Product
from .utils import get_user_carts


class CartAddView(View):
    def post(self, req):
        product_id = req.POST.get('product_id')
        product = Product.objects.get(id=product_id)

        if req.user.is_authenticated:
            carts = Cart.objects.filter(user=req.user, product=product)
            if carts.exists():
                cart = carts.first()
                if cart:
                    cart.quantity += 1
                    cart.save()
            else:
                Cart.objects.create(user=req.user, product=product, quantity=1)
        else:
            carts = Cart.objects.filter(session_key=req.session.session_key, product=product)
            if carts.exists():
                cart = carts.first()
                if cart:
                    cart.quantity += 1
                    cart.save()
            else:
                Cart.objects.create(session_key=req.session.session_key, product=product, quantity=1)
        users_cart = get_user_carts(req)
        cart_items_html = render_to_string(
            'cart/includes/cart_main_part.html', {'carts': users_cart}, request=req
        )
        response_data = {
            'message': 'Товар успешно добавлен в корзину',
            'cart_items_html': cart_items_html
        }
        return JsonResponse(response_data)


class CartChangeView(View):
    def post(self, req):
        cart_id = req.POST.get('cart_id')
        quantity = req.POST.get('quantity')

        cart = Cart.objects.get(id=cart_id)

        cart.quantity = quantity
        cart.save()

        cart = get_user_carts(req)
        cart_items_html = render_to_string(
            'cart/includes/cart_main_part.html', {'carts': cart}, request=req
        )
        response_data = {
            'message': 'Товар успешно добавлен в корзину',
            'cart_items_html': cart_items_html,
            'quantity': quantity
        }
        return JsonResponse(response_data)


class CartRemoveView(View):
    def post(self, req):
        cart_id = req.POST.get('cart_id')
        cart = get_object_or_404(Cart, id=cart_id)
        quantity = cart.quantity
        cart.delete()
        users_cart = get_user_carts(req)
        cart_items_html = render_to_string(
            'cart/includes/cart_main_part.html', {'carts': users_cart}, request=req
        )
        response_data = {
            'message': 'Товар успешно добавлен в корзину',
            'cart_items_html': cart_items_html,
            'quantity_deleted': quantity
        }
        return JsonResponse(response_data)


