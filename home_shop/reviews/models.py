from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models import Min

from catalog.models import Product
from orders.models import Order, OrderItem


class ProductReview(models.Model):
    STATUS_CHOICES = [
        ('moderating', 'На модерации'),
        ('published', 'Опубликован'),
        ('cancelled', 'Отклонен'),
    ]

    REJECTION_REASONS = [
        ('-', '-'),
        ('spam', 'Спам или реклама'),
        ('false_info', 'Ложная информация о продукте'),
        ('misleading', 'Вводящие в заблуждение сведения'),
        ('no_details', 'Отсутствие конкретики ("хороший/плохой")'),
        ('advertising', 'Реклама конкурентов'),
        ('off_topic', 'Не относится к продукту'),
        ('duplicate', 'Дублирующий отзыв'),
        ('offensive', 'Оскорбительные высказывания'),
        ('personal_data', 'Раскрытие персональных данных'),
        ('delayed', 'Отзыв опубликуется спустя 14 дней после первой покупки')
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews", verbose_name='Товар')
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='product_reviews',
                             verbose_name='Автор отзыва')
    rating = models.PositiveSmallIntegerField(default=5, verbose_name='Оценка')
    text = models.TextField(verbose_name='Текст отзыва')
    is_purchased = models.BooleanField(default=True, verbose_name='Куплен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='moderating',
                              verbose_name='Статус проверки')
    reason_for_cancel = models.CharField(max_length=50, choices=REJECTION_REASONS, default='-',
                                         verbose_name='Причина отказа')

    class Meta:
        db_table = 'product_reviews'
        ordering = ['-created_at']
        unique_together = ('product', 'user')
        verbose_name = 'Отзыв о товаре'
        verbose_name_plural = 'Отзывы о товарах'

    @property
    def days_since_created(self):
        first_order_date = OrderItem.objects.filter(
            product=self.product,
            order__user=self.user
        ).aggregate(first_date=Min('created_at'))['first_date']
        return (self.created_at - first_order_date).days

    def __str__(self):
        return f"{self.user} → {self.product} ({self.rating}/5)"


class OrderReview(models.Model):
    STATUS_CHOICES = [
        ('moderating', 'На модерации'),
        ('published', 'Опубликован'),
        ('cancelled', 'Отклонен'),
    ]

    REJECTION_REASONS = [
        ('-', '-'),
        ('spam', 'Спам или реклама'),
        ('false_info', 'Ложная информация о продукте'),
        ('misleading', 'Вводящие в заблуждение сведения'),
        ('no_details', 'Отсутствие конкретики ("хороший/плохой")'),
        ('advertising', 'Реклама конкурентов'),
        ('off_topic', 'Не относится к продукту'),
        ('duplicate', 'Дублирующий отзыв'),
        ('offensive', 'Оскорбительные высказывания'),
        ('personal_data', 'Раскрытие персональных данных'),
    ]

    order = models.OneToOneField(to=Order, on_delete=models.CASCADE, related_name="review")
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name="order_reviews")  # дублируем для удобства
    rating = models.PositiveSmallIntegerField(default=5, verbose_name='Оценка')
    text = models.TextField(verbose_name='Текст отзыва')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='На модерации',
                              verbose_name='Статус проверки')
    reason_for_cancel = models.CharField(max_length=50, choices=REJECTION_REASONS, default='-',
                                         verbose_name='Причина отказа')

    class Meta:
        ordering = ['-created_at']
        db_table = 'order_reviews'
        verbose_name = 'Отзыв о заказе'
        verbose_name_plural = 'Отзывы о заказах'

    def __str__(self):
        return f"Отзыв на заказ #{self.order.id} от {self.user}"
