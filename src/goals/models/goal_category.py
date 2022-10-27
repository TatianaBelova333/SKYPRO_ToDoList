from django.db import models
from django.utils import timezone

from core.models import User
from goals.models import DatesModelMixin


class GoalCategory(DatesModelMixin):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT, related_name='categories')
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)
