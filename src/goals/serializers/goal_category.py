from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from core.serializers import UserProfileSerializer
from goals.models import Board, BoardParticipant
from goals.models.goal_category import GoalCategory


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new GoalCategory instance."""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ["id", "created", "updated", "user"]
        fields = "__all__"

    def validate_board(self, board: Board) -> Board:
        """Validate the board field.

        Args:
            board (:obj:`Board`): Board instance.

        Returns:
            Board instance if the is_deleted field is False. Raises ValidationError otherwise.

        """
        if board.is_deleted:
            raise serializers.ValidationError("Not allowed in deleted board")
        return board

    def create(self, validated_data: dict) -> GoalCategory:
        """Creates a new GoalCategory instance if the current user is in the board participants list of the related board
        with the owner or writer role."""

        user = validated_data["user"]
        board = validated_data["board"]
        if not board.participants.filter(
            user=user, role__in=(BoardParticipant.Role.owner, BoardParticipant.Role.writer)
        ):
            raise PermissionDenied("У Вас нет права создавать категорию для данной доски.")
        category = GoalCategory.objects.create(**validated_data)
        return category


class GoalCategorySerializer(serializers.ModelSerializer):
    """Serializer for a GoalCategory instance."""

    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user", "board")
