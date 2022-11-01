from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, filters
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from goals.models import Board, Goal, Status
from goals.permissions import BoardPermissions
from goals.serializers import BoardSerializer, BoardCreateSerializer


class BoardCreateView(CreateAPIView):
    """Create a new board"""
    model = Goal
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardCreateSerializer


class BoardView(RetrieveUpdateDestroyAPIView):
    model = Board
    permission_classes = [permissions.IsAuthenticated, BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, board: Board):
        """Change the is_deleted fields of the board and board categories to True, as well as the status field of the
        board goals to False instead of their permanent deletion"""
        with transaction.atomic():
            board.is_deleted = True
            board.save()
            board.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=board).update(
                status=Status.archived
            )
        return board


class BoardListView(ListAPIView):
    """Return a list of the boards available to the current user"""
    model = Board
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    ordering_fields = ["title", "created", "updated"]
    search_fields = ["title"]

    def get_queryset(self):
        """Return queryset with boards filtered by current user"""
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)
