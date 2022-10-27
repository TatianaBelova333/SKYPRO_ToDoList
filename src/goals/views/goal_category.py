from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, filters
from rest_framework.pagination import LimitOffsetPagination

from goals.models import GoalCategory
from goals.models.goal import Status
from goals.serializers import GoalCategorySerializer, GoalCategoryCreateSerializer


class GoalCategoryCreateView(CreateAPIView):
    """Create a new goal category"""
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    """Return a list of all current user's active goal categories"""
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        """Return queryset with goal categories filtered by current user and is_deleted status"""
        return GoalCategory.objects.filter(
            user=self.request.user, is_deleted=False
        )


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    """Return, update and archive current user's goal categories"""

    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return queryset with goal categories filtered by current user and is_deleted status"""
        return GoalCategory.objects.filter(user=self.request.user, is_deleted=False)

    def perform_destroy(self, category: GoalCategory):
        """Change the category is_deleted status to False instead of deleting"""
        category.is_deleted = True
        for goal in category.goals.all():
            goal.status = Status.archived
            goal.save()
        category.save()
        return category
