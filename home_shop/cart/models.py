from django.db import models

from django.conf import settings

from catalog.models import Product


class CartQuerySet(models.QuerySet):
    def get_total_price(self):
        if self:
            return round(sum(cart.get_sum() for cart in self), 2)
        return 0

    def get_total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='carts', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')
    quantity = models.IntegerField(default=0, verbose_name='Количество')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='carts', verbose_name='Товар')
    add_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    session_key = models.CharField(max_length=32, blank=True, null=True, verbose_name='Ключ сессии')

    objects = CartQuerySet().as_manager()

    class Meta:
        db_table = 'carts'
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def get_sum(self):
        return round(self.product.get_total_price() * self.quantity, 2)

    def __str__(self):
        if self.user:
            return f'Корзина пользователя {self.user.username} | Товар: {self.product.name} | Количество: {self.quantity}'
        return f'Анонимная корзина | Товар: {self.product.name} | Количество: {self.quantity}'
# Create your models here.
