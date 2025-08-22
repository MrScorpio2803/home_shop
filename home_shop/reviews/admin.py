from django.contrib import admin
from .models import ProductReview, OrderReview

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    ...

@admin.register(OrderReview)
class OrderReviewAdmin(admin.ModelAdmin):
    ...
