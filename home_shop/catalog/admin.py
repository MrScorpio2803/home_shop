from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'quantity', 'price', 'discount', 'get_category']
    list_editable = ['price', 'discount', 'quantity']
    search_fields = ['name', 'description']
    list_filter = ['discount', 'quantity', 'category']
    fields = [
        'name',
        'category',
        'slug',
        'description',
        'image',
        ('price', 'discount'),
        'quantity'
    ]

    @admin.display(description='Категория')
    def get_category(self, obj):
        url = reverse('admin:catalog_category_change', args=[obj.category.id])
        return format_html('<a href="{}">{}</a>', url, obj.category.name)