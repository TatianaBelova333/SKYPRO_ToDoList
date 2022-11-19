from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, filters
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from goals.filters import GoalDateFilter
from goals.models.goal import Goal
from goals.models.goal import Status
from goals.permissions import GoalPermissions
from goals.serializers import GoalSerializer, GoalCreateSerializer
from django.db.models import QuerySet


class GoalListView(ListAPIView):
    """Return a list of goals of the boards to which the current user has access as a board participant"""

    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_class = GoalDateFilter
    ordering_fields = ["-priority", "due_date"]
    ordering = ["-priority", "due_date"]
    search_fields = ["title"]

    def get_queryset(self) -> QuerySet[Goal]:
        """Return queryset of all Goal instances excluding those with archived status to which the current user has
        access as a board participant"""

        return Goal.objects.filter(
            category__board__participants__user=self.request.user
        ).exclude(status=Status.archived)


class GoalCreateView(CreateAPIView):
    """Create a new Goal instance"""

    model = Goal
    permission_classes = [permissions.IsAuthenticated, GoalPermissions]
    serializer_class = GoalCreateSerializer


class GoalView(RetrieveUpdateDestroyAPIView):
    """Goal Retrieve/Update/Destroy APIView

    get:
    Return the given Goal instance.

    put:
    Update the given Goal instance.

    patch:
    Partially update the given Goal instance.

    delete:
    Update the status field of the given Goal instance to Status.archived.
    """

    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated, GoalPermissions]

    def get_queryset(self) -> QuerySet[Goal]:
        """Return queryset of all Goal instances excluding those with archived status to which the current user has
        access as a board participant"""
        return Goal.objects.filter(
            category__board__participants__user=self.request.user
        ).exclude(status=Status.archived)

    def perform_destroy(self, goal: Goal) -> Goal:
        """Change the goal status to 'archived' instead of deleting"""
        goal.status = Status.archived
        goal.save()
        return goal
