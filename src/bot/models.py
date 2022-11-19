from django.db import models

from core.models import User


class TgUser(models.Model):
    """Telegram user db model.

    Attributes:
        tg_chat_id (int): Unique identifier for the Telegram chat.
        tg_user_id (int): Unique identifier for the Telegram user.
        user (int, optional): User db model id. None if the user's web application account is not verified.
        verification_code (str): Verification code sent to the Telegram user to verify their web application account.
        is_verified (bool): True if the user's web application account is not verified. False otherwise.

    """
    class Meta:
        verbose_name = "Телеграм-пользователь"
        verbose_name_plural = "Телеграм-пользователь"

    tg_chat_id = models.BigIntegerField(verbose_name='Telegram chat-id')
    tg_user_id = models.BigIntegerField(verbose_name='Telegram user-id')
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=6, verbose_name='Код подтверждения')
    is_verified = models.BooleanField(default=False, verbose_name='Подтвержден')

