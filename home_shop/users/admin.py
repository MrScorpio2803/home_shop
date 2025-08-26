from django.contrib import admin

from cart.admin import CartTabAdmin
from orders.admin import OrderTabulareAdmin
from feedback.admin import FeedbackMesTabAdmin
from reviews.admin import OrderReviewTabularAdmin, ProductReviewTabularAdmin

from users.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    inlines = [CartTabAdmin, OrderTabulareAdmin, FeedbackMesTabAdmin, OrderReviewTabularAdmin, ProductReviewTabularAdmin]

# Register your models here.
