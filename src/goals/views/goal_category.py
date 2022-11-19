from django.db.models import QuerySet
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
    """Create a new GoalCategory instance."""

    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    """Return a list of all the GoalCategory instances to which the current user has access as a board participant."""

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

    def get_queryset(self) -> QuerySet[GoalCategory]:
        """Return a list of all the GoalCategory instances with False is_deleted field to which the current user has
        access as a board participant."""

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
    """GoalCategory Retrieve/Update/Destroy APIView

    get:
    Return the given GoalCategory instance.

    put:
    Update the given oalCategory instance.

    patch:
    Partially update the given oalCategory instance.

    delete:
    Update the is_deleted field of the given GoalCategory instance to True.
    """

    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [permissions.IsAuthenticated, CategoryPermissions]

    def get_queryset(self) -> QuerySet[GoalCategory]:
        """Return a list of all the GoalCategory instances with False is_deleted field to which the current user has
        access as a board participant."""
        return GoalCategory.objects.filter(board__participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, category: GoalCategory) -> GoalCategory:
        """Update the is_deleted fields of the given GoalCategory instance and related Goal instances to True."""
        with transaction.atomic():
            category.is_deleted = True
            category.save()
            category.goals.update(status=Status.archived)
        return category
