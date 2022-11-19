from django.db.models import QuerySet
from rest_framework import permissions, filters
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from goals.models.goal_comment import GoalComment
from goals.permissions import CommentsPermissions
from goals.serializers import GoalCommentCreateSerializer
from goals.serializers import GoalCommentSerializer


class GoalCommentListView(ListAPIView):
    """Return a list of GoalComment instances related to the Goal instance to which the current user has access as a
    board participant."""

    model = GoalComment
    serializer_class = GoalCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created", "updated"]
    ordering = ["-created"]

    def get_queryset(self) -> QuerySet[GoalComment]:
        """Return a list of GoalComment instances related to the Goal instance to which the current user has access as a
        board participant."""
        goal = self.request.query_params.get('goal')
        return GoalComment.objects.filter(goal=goal)


class GoalCommentCreateView(CreateAPIView):
    """Create a new GoalComment instance."""

    model = GoalComment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentCreateSerializer


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    """GoalComment Retrieve/Update/Destroy APIView

    get:
    Return the given GoalComment instance.

    put:
    Update the given GoalComment instance.

    patch:
    Partially update the given GoalComment instance.

    delete:
    Deletes the given GoalComment instance.

    """

    model = GoalComment
    serializer_class = GoalCommentSerializer
    permission_classes = [permissions.IsAuthenticated, CommentsPermissions]

    def get_queryset(self) -> QuerySet[GoalComment]:
        """Return a list of GoalComment instances related to the Goal instance to which the current user has access as a
        board participant."""
        return GoalComment.objects.filter(user=self.request.user)
