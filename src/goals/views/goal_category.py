from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, filters
from rest_framework.pagination import LimitOffsetPagination
from django.db import transaction
from goals.filters import BoardGoalCategoryFilter
from goals.models.goal_category import GoalCategory
from goals.models.goal import Status
from goals.permissions import CategoryPermissions
from goals.serializers import GoalCategorySerializer, GoalCategoryCreateSerializer


class GoalCategoryCreateView(CreateAPIView):
    """Create a new goal category"""
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated, CategoryPermissions]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    """Return a list of all current user's active goal categories"""
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_class = BoardGoalCategoryFilter
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        """Return queryset with goal categories filtered by current user and is_deleted status"""
        user = self.request.user
        board = self.request.query_params.get('board')
        if board:
            return GoalCategory.objects.filter(
                board=board,
                is_deleted=False,
            )
        else:
            return GoalCategory.objects.filter(
                board__participants__user=user,
                is_deleted=False,
            )


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    """Return, update and archive current user's goal categories"""

    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [permissions.IsAuthenticated, CategoryPermissions]

    def get_queryset(self):
        """Return queryset with goal categories filtered by current user and is_deleted status"""
        return GoalCategory.objects.filter(board__participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, category: GoalCategory):
        """Change the category is_deleted status to False instead of deleting"""
        with transaction.atomic():
            category.is_deleted = True
            category.save()
            category.goals.update(status=Status.archived)
        return category
