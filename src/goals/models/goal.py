from django.db import models
from core.models import User
from goals.models.goal_category import GoalCategory
from goals.models.basemixin import DatesModelMixin


class Status(models.IntegerChoices):
    to_do = 1, "К выполнению"
    in_progress = 2, "В процессе"
    done = 3, "Выполнено"
    archived = 4, "Архив"


class Priority(models.IntegerChoices):
    low = 1, "Низкий"
    medium = 2, "Средний"
    high = 3, "Высокий"
    critical = 4, "Критический"


class Goal(DatesModelMixin):
    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"

    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT, related_name='goals')
    title = models.CharField(verbose_name="Заголовок", max_length=255)
    description = models.TextField(verbose_name="Описание", null=True, blank=True, default='')
    due_date = models.DateTimeField(verbose_name="Дата выполнения", null=True)
    status = models.PositiveSmallIntegerField(verbose_name="Статус", choices=Status.choices, default=Status.to_do)
    priority = models.PositiveSmallIntegerField(
        verbose_name="Приоритет", choices=Priority.choices, default=Priority.medium
    )
    category = models.ForeignKey(
        GoalCategory,
        verbose_name="Категория",
        on_delete=models.PROTECT,
        related_name='goals',
    )
