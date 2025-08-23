from django.db import models
from django.conf import settings


class FeedbackMessage(models.Model):
    TOPIC_CHOICES = [
        ('order', 'Вопрос по заказу'),
        ('product', 'Вопрос по товару'),
        ('complaint', 'Жалоба'),
        ('suggestion', 'Предложение'),
        ('other', 'Другое'),
    ]
    STATUS_CHOICES = [
        ("new", "Новое"),
        ("in_progress", "В работе"),
        ("answered", "Отвечено"),
        ("closed", "Закрыто"),
        ("archived", "В архиве"),
    ]

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_DEFAULT,
        default=None,
        null=True,
        blank=True,
        help_text="Авторизованный пользователь (если есть)"
    )
    name = models.CharField(max_length=255, verbose_name='Имя отправителя')
    email = models.EmailField(verbose_name="Email")

    topic = models.CharField(
        max_length=20,
        choices=TOPIC_CHOICES,
        default='order',
        verbose_name="Тема обращения"
    )
    custom_topic = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Тема не из списка"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name="Статус обращения"
    )

    text = models.TextField(verbose_name="Текст обращения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата обращения')

    class Meta:
        db_table = 'feedback_messages'
        verbose_name = "Обращение"
        verbose_name_plural = "Обращения"
