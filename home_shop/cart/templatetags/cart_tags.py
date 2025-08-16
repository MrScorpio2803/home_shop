from django import template
from cart.utils import get_user_carts

register = template.Library()


@register.simple_tag
def user_carts(req):
    if req.user.is_authenticated:
        return get_user_carts(req)
