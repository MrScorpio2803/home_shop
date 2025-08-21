from django.db import models

from django.conf import settings

from catalog.models import Product

class OrderItemQuerySet(models.QuerySet):
    
    def get_total_price(self):
        if self:
            return sum(item.total_cost() for item in self)
        return 0

    def get_total_quantity(self):
        if self:
            return sum(item.quantity for item in self)
        return 0

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('completed', 'Завершён'),
        ('cancelled', 'Отменён'),
    ]
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_DEFAULT, verbose_name='Пользователь', default=None)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона')
    delivery = models.BooleanField(default=False, verbose_name='Требуется доставка?')
    delivery_address = models.TextField(null=True, blank=True, verbose_name='Адрес доставки')
    is_payment_on_get = models.BooleanField(default=False, verbose_name='Оплата при получении')
    is_paid = models.BooleanField(default=False, verbose_name='Статус оплаты')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='В обработке', verbose_name='Статус заказа')

    class Meta:
        db_table = 'orders'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
    
    def __str__(self) -> str:
        return f'Заказ № {self.pk}. Заказчик {self.user.first_name} {self.user.last_name}'
    

class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name='Заказ', related_name='items')
    product = models.ForeignKey(to=Product, on_delete=models.SET_DEFAULT, blank=True, null=True, verbose_name='Товар', default=None)
    name = models.CharField(max_length=150, verbose_name='Название')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата продажи')

    class Meta:
        db_table = 'order_item'
        verbose_name = 'Проданный товар'
        verbose_name_plural = 'Проданные товары'
    
    objects = OrderItemQuerySet.as_manager()
    
    def total_cost(self):
        return round(self.price * self.quantity , 2)
    

    def __str__(self) -> str:
        return f'Товар {self.name} | Количество {self.quantity} | Стоимость {self.total_cost()} | Заказ {self.order.pk}'


