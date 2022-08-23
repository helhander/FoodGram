from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing',
        verbose_name='Автор',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='unique_subscription',
                fields=['subscriber', 'author'],
            ),
            models.CheckConstraint(
                check=~models.Q(subscriber=models.F('author')),
                name='subscriber_is_not_author',
            ),
        ]
