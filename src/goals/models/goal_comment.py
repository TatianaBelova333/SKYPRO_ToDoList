from django.db import models
from core.models import User
from goals.models.basemixin import DatesModelMixin
from goals.models.goal import Goal


class GoalComment(DatesModelMixin):
    """Goal comment db model class."""

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.CASCADE, related_name='comments')
    text = models.CharField(verbose_name="Текст", max_length=255)
    goal = models.ForeignKey(Goal, verbose_name="Цель", on_delete=models.CASCADE, related_name='comments')
