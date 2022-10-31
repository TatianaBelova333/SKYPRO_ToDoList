from rest_framework import serializers
from core.serializers import UserProfileSerializer
from goals.models.goal import Goal
from goals.models.goal_category import GoalCategory


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    description = serializers.CharField(required=False)

    class Meta:
        model = Goal
        read_only_fields = ["id", "created", "updated", "user"]
        fields = "__all__"

    def validate_category(self, category: GoalCategory):
        if category.is_deleted:
            raise serializers.ValidationError("not allowed in deleted category")
        return category


class GoalSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")
