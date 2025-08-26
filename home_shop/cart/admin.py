from django.contrib import admin
from .models import Cart


class CartTabAdmin(admin.TabularInline):
    model = Cart
    fields = ['product', 'quantity', 'add_at']
    search_fields = ['product', 'add_at']
    readonly_fields = ('add_at',)
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['display_user', 'display_product', 'quantity', 'add_at']
    list_filter = ['user', 'product__name', 'add_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__phone', 'product__name']

    @admin.display(description='Пользователь')
    def display_user(self, obj):
        if obj.user:
            return str(obj.user.username)
        return 'Аноним'

    @admin.display(description='Товар')
    def display_product(self, obj):
        return str(obj.product.name)
