from django.db import models
from core.models import User
from goals.models.basemixin import DatesModelMixin
from goals.models.board import Board


class GoalCategory(DatesModelMixin):
    """Goal category db model class."""

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT, related_name='categories')
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)
    board = models.ForeignKey(
        Board, verbose_name="Доска", on_delete=models.PROTECT, related_name="categories"
    )
