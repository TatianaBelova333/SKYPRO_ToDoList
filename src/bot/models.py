from django.db import models

from core.models import User


class TgUser(models.Model):
    class Meta:
        verbose_name = "Телеграм-пользователь"
        verbose_name_plural = "Телеграм-пользователь"

    tg_chat_id = models.BigIntegerField(verbose_name='Telegram chat-id')
    tg_user_id = models.BigIntegerField(verbose_name='Telegram user-id')
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=6, verbose_name='Код подтверждения')
    is_verified = models.BooleanField(default=False, verbose_name='Подтвержден')

