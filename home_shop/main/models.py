from django.db import models
from django.conf import settings


class Review(models.Model):
    class Meta:
        db_table = 'reviews'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='authors', null=True, blank=True, verbose_name='Автор отзыва')

    def __str__(self):
        return f'Автор отзыва: {self.author.username}. Начало отзыва: {self.text[:30]}'

