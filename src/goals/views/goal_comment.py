from rest_framework import permissions, filters
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from goals.models import GoalComment
from goals.serializers import GoalCommentCreateSerializer
from goals.serializers import GoalCommentSerializer


class GoalCommentListView(ListAPIView):
    """Return a list of comments filtered by the current user and the goal"""
    model = GoalComment
    serializer_class = GoalCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [
        filters.OrderingFilter,
    ]
    ordering_fields = ["created", "updated"]
    ordering = ["-created"]

    def get_queryset(self):
        """Return queryset with goal categories filtered by current user and is_deleted status"""
        goal = self.request.query_params.get('goal')
        return GoalComment.objects.filter(user=self.request.user, goal=goal)


class GoalCommentCreateView(CreateAPIView):
    """Create a new comment to the goal"""
    model = GoalComment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCommentCreateSerializer


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    """Return, update or delete current user's comments to a specific goal"""
    model = GoalComment
    serializer_class = GoalCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return queryset with all the current user's comments"""
        return GoalComment.objects.filter(user=self.request.user)
