from django import template
from cart.utils import get_user_carts, get_user_orders, get_order_items

register = template.Library()


@register.simple_tag
def user_carts(req):
    return get_user_carts(req)


@register.simple_tag
def user_orders(req):
    return get_user_orders(req)


@register.simple_tag
def order_items(req, order_id):
    return get_order_items(req, order_id)
