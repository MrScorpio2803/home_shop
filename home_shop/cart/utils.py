from .models import Cart
from orders.models import Order, OrderItem

def get_user_carts(req):
    if req.user.is_authenticated:
        return Cart.objects.filter(user=req.user)

    if not req.session.session_key:
        req.session.create()
    return Cart.objects.filter(session_key=req.session.session_key)


def get_user_orders(req):
    return Order.objects.filter(user=req.user).prefetch_related('items')
