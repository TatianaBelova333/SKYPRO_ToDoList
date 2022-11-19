from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from core.serializers import UserProfileSerializer
from goals.models import Goal, Status, BoardParticipant
from goals.models.goal_comment import GoalComment


class GoalCommentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new GoalComment instance."""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        read_only_fields = ["id", "created", "updated", "user"]
        fields = "__all__"

    def validate_goal(self, goal: Goal) -> Goal:
        """Validate the goal field.

        Args:
            goal (:obj:`Goal`): Goal instance.

        Returns:
            Goal instance if the status is archived. Raises ValidationError otherwise.

        """
        if goal.status == Status.archived:
            raise serializers.ValidationError("Not allowed in deleted goal")
        return goal

    def create(self, validated_data: dict) -> GoalComment:
        """Creates a new GoalComment instance if the current user is in the board participants list of the related board
        with the owner or writer role."""

        user = validated_data["user"]
        goal = validated_data["goal"]
        board = goal.category.board
        if not board.participants.filter(
            user=user, role__in=(BoardParticipant.Role.owner, BoardParticipant.Role.writer)
        ):
            raise PermissionDenied("У Вас нет права добавлять комментарии к данной цели")
        comment = GoalComment.objects.create(**validated_data)
        return comment


class GoalCommentSerializer(serializers.ModelSerializer):
    """Serializer for a GoalComment instance."""

    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = GoalComment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user", "goal")
