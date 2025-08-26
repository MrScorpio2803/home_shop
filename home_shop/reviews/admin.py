from typing import Any
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import ProductReview, OrderReview

from orders.models import OrderItem

class ProductReviewTabularAdmin(admin.TabularInline):
    model = ProductReview
    fields = ['product', 'text', 'rating', 'status', 'reason_for_cancel']
    search_fields = ['text', 'reason_for_cancel']
    readonly_fields = ('created_at',)
    extra = 1

class OrderReviewTabularAdmin(admin.TabularInline):
    model = ProductReview
    fields = ['id', 'text', 'rating', 'status', 'reason_for_cancel']
    search_fields = ['text', 'reason_for_cancel']
    readonly_fields = ('created_at',)
    extra = 1


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    
    list_display = ['get_name', 'get_product', 'rating', 'text', 'updated_at', 'days_after_review', 'is_purchased', 'status', 'reason_for_cancel']
    list_editable = ['status', 'reason_for_cancel']
    search_fields = ['user__phone', 'text', 'product__name']
    list_filter = ['status', 'user', 'is_purchased', 'reason_for_cancel', 'updated_at']


    @admin.display(description='Имя пользователя')
    def get_name(self, obj):
        return obj.user.first_name
    
    @admin.display(description='Товар')
    def get_product(self, obj):
        url = reverse('admin:catalog_product_change', args=[obj.product.id])
        return format_html('<a href="{}">{}</a>', url, obj.product.name)
    
    @admin.display(description='Кол-во дней после отправки отзыва')
    def days_after_review(self, obj):
        return obj.days_since_created
    
    

@admin.register(OrderReview)
class OrderReviewAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'get_phone', 'get_id_order', 'get_items', 'rating', 'text', 'updated_at', 'status', 'reason_for_cancel']
    list_editable = ['status', 'reason_for_cancel']
    search_fields = ['user__phone', 'order__id', 'text']
    list_filter = ['user__phone', 'order__id', 'rating', 'status', 'reason_for_cancel']

    @admin.display(description='Товары в заказе')
    def get_items(req, obj):
        items = [item.name for item in OrderItem.objects.filter(order=obj.order)]
        return ', '.join(items)
    
    @admin.display(description='Имя пользователя')
    def get_name(self, obj):
        return obj.user.first_name
    
    @admin.display(description='Номер телефона')
    def get_phone(self, obj):
        return obj.user.phone
    
    @admin.display(description='Номер заказа')
    def get_id_order(self, obj):
        url = reverse('admin:orders_order_change', args=[obj.order.id])
        return format_html('<a href="{}">{}</a>', url, obj.order.id)
    
