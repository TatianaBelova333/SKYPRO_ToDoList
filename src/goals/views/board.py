from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, filters
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from goals.models import Board, Goal, Status
from goals.permissions import BoardPermissions
from goals.serializers import BoardSerializer, BoardCreateSerializer
from django.db.models import QuerySet


class BoardCreateView(CreateAPIView):
    """Create a new Board instance"""

    model = Goal
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardCreateSerializer


class BoardView(RetrieveUpdateDestroyAPIView):
    """Board Retrieve/Update/Destroy APIView

    get:
    Return the given Board instance.

    put:
    Update the given Board instance.

    patch:
    Partially update the given Board instance.

    delete:
    Update the is_deleted field of the given Board instance to True.
    """

    model = Board
    permission_classes = [permissions.IsAuthenticated, BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self) -> QuerySet[Board]:
        """Return queryset of the boards to which the current user has access as a board participant"""
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, board: Board):
        """Update the is_deleted field of the given Board instance and related Board Categories to True, as well as
        the status field of the related Category Goals to archived"""
        with transaction.atomic():
            board.is_deleted = True
            board.save()
            board.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=board).update(
                status=Status.archived
            )
        return board


class BoardListView(ListAPIView):
    """Return a list of the Board instances to which the current user has access as a board participant"""

    model = Board
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    ordering_fields = ["title", "created", "updated"]
    search_fields = ["title"]

    def get_queryset(self) -> QuerySet[Board]:
        """Return queryset of the boards to which the current user has access as a board participant"""
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)
