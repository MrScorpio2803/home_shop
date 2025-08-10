import datetime

from django.db import models


class Product(models.Model):
    class Meta:
        db_table = 'products'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="images/goods/", blank=True, null=True)
    price = models.FloatField()
    discount = models.FloatField(default=0)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    slug = models.SlugField()
    created_at = models.DateTimeField(default=datetime.datetime.now())


class Category(models.Model):
    class Meta:
        db_table = 'categories'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    key = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

# Create your models here.
