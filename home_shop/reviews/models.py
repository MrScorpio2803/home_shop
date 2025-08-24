from django.db import models
from django.conf import settings
from django.utils import timezone

from catalog.models import Product
from orders.models import Order


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews", verbose_name='Товар')
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='product_reviews',
                             verbose_name='Автор отзыва')
    rating = models.PositiveSmallIntegerField(default=5, verbose_name='Оценка')
    text = models.TextField(verbose_name='Текст отзыва')
    is_purchased = models.BooleanField(default=True, verbose_name='Куплен')
    is_published = models.BooleanField(default=False, verbose_name='Опубликован')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')

    class Meta:
        db_table = 'product_reviews'
        ordering = ['-created_at']
        unique_together = ('product', 'user')

    @property
    def days_since_created(self):
        return (timezone.now() - self.created_at).days

    def __str__(self):
        return f"{self.user} → {self.product} ({self.rating}/5)"


class OrderReview(models.Model):
    order = models.OneToOneField(to=Order, on_delete=models.CASCADE, related_name="review")
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name="order_reviews")  # дублируем для удобства
    rating = models.PositiveSmallIntegerField(default=5, verbose_name='Оценка')
    text = models.TextField(verbose_name='Текст отзыва')
    is_published = models.BooleanField(default=True, verbose_name='Опубликован')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')

    class Meta:
        ordering = ['-created_at']
        db_table = 'order_reviews'

    def __str__(self):
        return f"Отзыв на заказ #{self.order.id} от {self.user}"
