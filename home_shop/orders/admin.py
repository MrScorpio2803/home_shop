import datetime
from django.http import HttpResponse
import pandas as pd

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Order, OrderItem

from home_shop.utils import action

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
    
    actions = ['make_paid', 'send', 'complete', 'analyze_orders', 'export_to_xlsx']

    @admin.display(description='Пользователь')
    def get_user(self, obj):
        url = reverse('admin:users_user_change', args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)

    @action('Пометить оплаченными')
    def make_paid(modeladmin, request, queryset):
        queryset.update(is_paid=True)
        modeladmin.message_user(request, f"Оплата принята у {queryset.count()} заказа(ов)")

    @action('Отправить')
    def send(modeladmin, request, queryset):
        queryset.update(status='shipped')
        modeladmin.message_user(request, f"Отправлено {queryset.count()} заказ(а/ов)")

    @action('Завершить')
    def complete(modeladmin, request, queryset):
        queryset.update(status='completed')
        modeladmin.message_user(request, f"Завершено {queryset.count()} заказ(а/ов)")
    
    @action('Быстрый анализ заказов')
    def analyze_orders(modeladmin, request, queryset):
        stats = {
            'new': queryset.filter(status='new').count(),
            'shipped': queryset.filter(status='shipped').count(),
            'completed': queryset.filter(status='completed').count(),
            'cancelled': queryset.filter(status='cancelled').count(),
            'with_delivery': queryset.filter(delivery=True).count(),
            'paid': queryset.filter(is_paid=True).count()
        }
        
        message = (f"Статистика по {queryset.count()} заказам:\n"
                f"Новых: {stats['new']} | Отправленных: {stats['shipped']}\n"
                f"Завершённых: {stats['completed']} | Отменённых: {stats['cancelled']}\n"
                f"С доставкой: {stats['with_delivery']} | Оплаченных: {stats['paid']}")
        
        modeladmin.message_user(request, message)
    
    @action('Экспорт в xlsx')
    def export_to_xlsx(modeladmin, request, queryset):
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        cur_date = datetime.datetime.now().strftime('%d_%m_%y_%H:%M')
        response['Content-Disposition'] = f'attachment; filename="export_orders_{cur_date}.xlsx"'
        data = []
        
        for message in queryset:
            cur_row = {
                'name': message.user.first_name,
                'phone': message.phone_number,
                'need_delivery': 'Нужна доставка' if message.delivery else 'Не нужна доставка',
                'addres': message.delivery_address if message.delivery else '-',
                'is_paid': 'Оплачен' if message.is_paid else 'Не оплачен',
                'status': message.get_status_display(),
                'date': message.created_at.strftime('%Y-%m-%d %H:%M'),
            }
            data.append(cur_row)
        df = pd.DataFrame(data)
        df.to_excel(response, index=False)
        return response

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['get_order', 'get_product', 'price', 'quantity', 'created_at']
    search_fields = ['order', 'product', 'name']
    list_filter = ['order', 'product__name', 'created_at']
    

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


