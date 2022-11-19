import django_filters
from django.db import models
from django_filters import rest_framework
from goals.models.goal_category import GoalCategory
from goals.models.goal import Goal


class GoalDateFilter(rest_framework.FilterSet):
    """Filter queryset of Goal instances by due_date, category, status and priority fields"""

    class Meta:
        model = Goal
        fields = {
            "due_date": ("lte", "gte"),
            "category": ("exact", "in"),
            "status": ("exact", "in"),
            "priority": ("exact", "in"),
        }

    filter_overrides = {
        models.DateTimeField: {"filter_class": django_filters.IsoDateTimeFilter},
    }


class BoardGoalCategoryFilter(rest_framework.FilterSet):
    """Filter queryset of GoalCategory instances by the board field"""

    class Meta:
        model = GoalCategory
        fields = {
            "board": ("exact", "in"),
        }
