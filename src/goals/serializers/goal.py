from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from core.serializers import UserProfileSerializer
from goals.models import BoardParticipant
from goals.models.goal import Goal
from goals.models.goal_category import GoalCategory


class GoalCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new Goal instance."""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    description = serializers.CharField(required=False)

    class Meta:
        model = Goal
        read_only_fields = ["id", "created", "updated", "user"]
        fields = "__all__"

    def validate_category(self, category: GoalCategory) -> GoalCategory:
        """Validate the category field.

        Args:
            category (:obj:`GoalCategory`): GoalCategory instance.
        Returns:
            GoalCategory instance if the is_deleted field is False. Raises ValidationError otherwise.
        """

        if category.is_deleted:
            raise serializers.ValidationError("Not allowed in deleted category")
        return category

    def create(self, validated_data: dict) -> Goal:
        """Creates a new Goal instance if the current user is in the board participants list of the related board
        with the owner or writer role."""

        user = validated_data["user"]
        category = validated_data["category"]
        board = category.board
        if not board.participants.filter(
            user=user, role__in=(BoardParticipant.Role.owner, BoardParticipant.Role.writer)
        ):
            raise PermissionDenied("У Вас нет права создавать цели для данной категории.")
        goal = Goal.objects.create(**validated_data)
        return goal


class GoalSerializer(serializers.ModelSerializer):
    """Serializer for a Goal instance."""

    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")
