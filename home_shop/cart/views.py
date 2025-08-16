from django.shortcuts import render, redirect
from django.views import View

from .models import Cart
from catalog.models import Product


def cart_add(req, product_slug):
    product = Product.objects.get(slug=product_slug)

    if req.user.is_authenticated:
        carts = Cart.objects.filter(user=req.user, product=product)
        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(user=req.user, product=product, quantity=1)
    return redirect(req.META['HTTP_REFERER'])


class CartChangeView(View):
    ...


class CartRemoveView(View):
    ...
