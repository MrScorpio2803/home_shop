from typing import Optional

from django.http import HttpRequest
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404

from catalog.models import Product

from .models import Cart
from .utils import get_user_carts


class CartMixin:
    def get_cart(self, request: HttpRequest, product: Optional[Product] = None, cart_id: int = None) -> Optional[Cart]:
        if cart_id:
            return get_object_or_404(Cart, id=cart_id)
        
        if request.user.is_authenticated:
            query_kwargs = {'user': request.user}
        else:
            query_kwargs = {'session_key': request.session.session_key}
        
        if product:
            query_kwargs['product'] = product
        
        return Cart.objects.filter(**query_kwargs).first()
    
    def render_cart(self, request: HttpRequest) -> str:
        users_cart = get_user_carts(request)
        cart_items_html = render_to_string(
            'cart/includes/cart_main_part.html', {'carts': users_cart}, request=request
        )
        return cart_items_html
