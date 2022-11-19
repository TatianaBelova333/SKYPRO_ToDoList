from django.db import transaction
from rest_framework import serializers
from core.models import User
from goals.models import Board, BoardParticipant


class BoardCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new Board instance"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        read_only_fields = ("id", "created", "updated")
        fields = "__all__"

    def create(self, validated_data: dict) -> Board:
        """Create a new Board instance and add the current user to the board participants with the owner role"""

        user = validated_data.pop("user")
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(
            user=user, board=board, role=BoardParticipant.Role.owner
        )
        return board


class BoardListSerializer(serializers.ModelSerializer):
    """Serializer for retrieving a list of Board instances"""

    class Meta:
        model = Board
        fields = "__all__"


class BoardParticipantSerializer(serializers.ModelSerializer):
    """Serializer for retrieving a BoardParticipant instance"""

    role = serializers.ChoiceField(required=True, choices=BoardParticipant.editable_choices)
    user = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())

    class Meta:
        model = BoardParticipant
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "board")


class BoardSerializer(serializers.ModelSerializer):
    """Serializer for retrieving a Board instance"""

    participants = BoardParticipantSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", 'user')

    def update(self, board: Board, validated_data: dict) -> Board:
        """Updates the retrieved Board instance and adds other users to the board participants"""

        owner = validated_data.pop("user")
        new_participants = validated_data.pop("participants")
        new_by_id = {part["user"].id: part for part in new_participants}

        old_participants = board.participants.exclude(user=owner)
        with transaction.atomic():
            for old_participant in old_participants:
                if old_participant.user_id not in new_by_id:
                    old_participant.delete()
                else:
                    if (
                            old_participant.role
                            != new_by_id[old_participant.user_id]["role"]
                    ):
                        old_participant.role = new_by_id[old_participant.user_id][
                            "role"
                        ]
                        old_participant.save()
                    new_by_id.pop(old_participant.user_id)
            for new_part in new_by_id.values():
                BoardParticipant.objects.create(
                    board=board, user=new_part["user"], role=new_part["role"]
                )

            board.title = validated_data["title"]
            board.save()

        return board
