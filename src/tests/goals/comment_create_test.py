import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework.exceptions import ErrorDetail
from goals.models import GoalComment, BoardParticipant


@pytest.mark.django_db
class TestGoalCommentCreateView:
    """GoalCommentCreateView tests"""

    def test_create_comment_success(self, client, current_board_participant, goal):
        """Test comment creation for authorised user with owner role"""

        user = current_board_participant.user

        client.force_login(user=user)

        data = {
            "text": "My test comment",
            "goal": goal.id,
        }
        response = client.post(
            data=data,
            path=reverse('goals:create_comment'),
            content_type='application/json',
        )

        comment = GoalComment.objects.last()

        assert response.status_code == 201
        assert response.data == {
            "id": comment.id,
            "created": timezone.localtime(comment.created).isoformat(),
            "updated": timezone.localtime(comment.updated).isoformat(),
            "text": "My test comment",
            "goal": goal.id,
        }

    def test_create_comment_unauthorised(self, client, goal):
        """Test comment creation for unauthorised user"""

        data = {
            "text": "My test comment",
            "goal": goal.id,
        }
        response = client.post(
            "/goals/goal_comment/create",
            data,
        )
        assert response.status_code == 401
        assert response.data == {'detail': ErrorDetail(
            string='Authentication credentials were not provided.',
            code='not_authenticated'
        )}

    def test_create_comment_reader(self, client, current_board_participant, goal):
        """Test comment creation for authorised user with reader role"""

        current_board_participant.role = BoardParticipant.Role.reader
        current_board_participant.save()
        user = current_board_participant.user

        client.force_login(user=user)

        data = {
            "text": "My test comment",
            "goal": goal.id,
        }
        response = client.post(
            data=data,
            path=reverse('goals:create_comment'),
            content_type='application/json',
        )

        assert response.status_code == 403
        assert response.data == {'detail': ErrorDetail(
            string='У Вас нет права добавлять комментарии к данной цели',
            code='permission_denied')
        }

    def test_create_comment_writer(self, client, current_board_participant, goal):
        """Test comment creation for authorised user with writer role"""

        current_board_participant.role = BoardParticipant.Role.writer
        current_board_participant.save()
        user = current_board_participant.user

        client.force_login(user=user)

        data = {
            "text": "My test comment",
            "goal": goal.id,
        }
        response = client.post(
            data=data,
            path=reverse('goals:create_comment'),
            content_type='application/json',
        )

        comment = GoalComment.objects.last()

        assert response.status_code == 201
        assert response.data == {
            "id": comment.id,
            "created": timezone.localtime(comment.created).isoformat(),
            "updated": timezone.localtime(comment.updated).isoformat(),
            "text": "My test comment",
            "goal": goal.id,
        }
