from django.db import models
from core.models import User
from goals.models.basemixin import DatesModelMixin
from goals.models.board import Board


class BoardParticipant(DatesModelMixin):
    """Board participant object class."""

    class Meta:
        unique_together = ("board", "user")
        verbose_name = "Участник"
        verbose_name_plural = "Участники"

    class Role(models.IntegerChoices):
        """Board participant role class."""

        owner = 1, "Владелец"
        writer = 2, "Редактор"
        reader = 3, "Читатель"

    editable_choices = [Role.writer, Role.reader]

    board = models.ForeignKey(
        Board,
        verbose_name="Доска",
        on_delete=models.PROTECT,
        related_name="participants",
    )
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.PROTECT,
        related_name="participants",
    )
    role = models.PositiveSmallIntegerField(
        verbose_name="Роль", choices=Role.choices, default=Role.owner
    )
