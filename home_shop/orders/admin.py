from django.contrib import admin
from .models import Order, OrderItem


class OrderTabulareAdmin(admin.TabularInline):
    model = Order
    fields = ('delivery', 'status', 'is_payment_on_get', 'is_paid', 'created_at')
    search_fields = ('delivery', 'is_payment_on_get', 'is_paid', 'created_at')
    readonly_fields = ('created_at',)
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'delivery',
        'delivery_address',
        'status',
        'is_payment_on_get',
        'is_paid',
        'created_at'
    ]
    search_fields = [
        'id',
        'created_at'
    ]
    readonly_fields = ('created_at',)
    list_editable = [
        'delivery',
        'delivery_address',
        'status',
        'is_payment_on_get',
        'is_paid'
    ]
    list_filter = [
        'delivery',
        'status',
        'is_payment_on_get',
        'user',
        'is_paid'
    ]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'price', 'quantity']
    search_fields = ['order', 'product', 'name']

