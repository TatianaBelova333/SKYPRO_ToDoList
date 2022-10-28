from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, filters
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView

from goals.filters import GoalDateFilter
from goals.models import Goal
from goals.models.goal import Status
from goals.serializers import GoalSerializer, GoalCreateSerializer


class GoalListView(ListAPIView):
    """Return a list of current user's goals"""
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
    ordering = ["-priority"]
    search_fields = ["title"]

    def get_queryset(self):
        """Return queryset with goal categories filtered by current user and is_deleted status"""
        return Goal.objects.filter(user=self.request.user).exclude(status=Status.archived)


class GoalCreateView(CreateAPIView):
    """Create a new goal category"""
    model = Goal
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCreateSerializer


class GoalView(RetrieveUpdateDestroyAPIView):
    """Return, update and archive current user's goals"""

    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return queryset with all the current user's goals except archived ones"""
        return Goal.objects.filter(user=self.request.user).exclude(status=Status.archived)

    def perform_destroy(self, goal: Goal):
        """Change the goal status to 'archived' instead of deleting"""
        goal.status = Status.archived
        goal.save()
        return goal
