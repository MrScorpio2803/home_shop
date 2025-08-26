from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

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
        'get_user',
        'phone_number',
        'delivery',
        'delivery_address',
        'status',
        'is_payment_on_get',
        'is_paid',
        'created_at'
    ]
    search_fields = [
        'id',
        'created_at',
        'phone_number',
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
        'is_paid',
        'created_at',
    ]
    @admin.display(description='Пользователь')
    def get_user(self, obj):
        url = reverse('admin:users_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['get_order', 'get_product', 'price', 'quantity']
    search_fields = ['order', 'product', 'name']
    list_filter = ['order', 'product__name']
    

    # @admin.display(description='Заказчик')
    # def get_user(self, obj):
    #     url = reverse('admin:users_user_change', args=[obj.user.id])
    #     return format_html('<a href="{}">{}</a>', url, obj.user.username)

    @admin.display(description='Номер заказа')
    def get_order(self, obj):
        return obj.order.id
    
    @admin.display(description='Товар')
    def get_product(self, obj):
        url = reverse('admin:catalog_product_change', args=[obj.product.id])
        return format_html('<a href="{}">{}</a>', url, obj.product.name)


