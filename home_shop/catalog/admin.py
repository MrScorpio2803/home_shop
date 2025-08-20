from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'quantity', 'price', 'discount', 'category']
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