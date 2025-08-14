import datetime
from decimal import Decimal

from django.db import models


class Product(models.Model):
    class Meta:
        db_table = 'products'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    name = models.CharField(max_length=100, verbose_name='Название товара')
    description = models.TextField(verbose_name='Описание товара')
    image = models.ImageField(upload_to="images/goods/", blank=True, null=True, verbose_name='Картинка для товара')
    price = models.FloatField(verbose_name='Начальная цена')
    discount = models.FloatField(default=0, verbose_name='Скидка')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products', null=True, blank=True, verbose_name='Категория товара')
    slug = models.SlugField()
    created_at = models.DateTimeField(default=datetime.datetime.now(), verbose_name='Дата добавления')

    def get_total_price(self):
        if self.discount > 0:
            return round(self.price * (1 - self.discount / 100), 2)
        return self.price


class Category(models.Model):
    class Meta:
        db_table = 'categories'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    key = models.CharField(max_length=100, verbose_name='Название категории')
    name = models.CharField(max_length=100, verbose_name='Название для отображения')
    slug = models.SlugField()
# Create your models here.
