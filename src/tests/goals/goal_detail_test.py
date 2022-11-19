import pytest
from django.utils import timezone
from rest_framework.exceptions import ErrorDetail
from core.serializers import UserProfileSerializer
from goals.models import Status, Goal, BoardParticipant
from goals.serializers import GoalSerializer
from tests.factories import UserFactory


@pytest.mark.django_db
class TestGoalView:
    """GoalView tests suite"""

    def test_goal_detail_unauthorised(self, client, current_user_goal):
        """Test for retrieving one goal by unauthorised user"""

        response = client.get(path=f"/goals/goal/{current_user_goal.id}")

        assert response.status_code == 401

    def test_goal_retrieve_view(self, client, current_board_participant, current_user_goal):
        """Test for retrieving a goal by current_board_participant with owner role"""

        client.force_login(user=current_board_participant.user)

        expected_response = GoalSerializer(current_user_goal).data

        response = client.get(path=f"/goals/goal/{current_user_goal.id}")

        assert response.status_code == 200
        assert response.data == expected_response

    def test_goal_update_view(self, client, current_board_participant, current_user_goal, current_user_category):
        """Test for retrieving and updating a goal by current_board_participant with owner role"""

        client.force_login(user=current_board_participant.user)

        data = {
            'title': 'Call home',
            "description": "call home tomorrow"
        }

        response = client.patch(
            path=f"/goals/goal/{current_user_goal.id}",
            data=data,
            content_type='application/json',
        )
        goal = Goal.objects.latest('updated')

        assert response.status_code == 200
        assert response.data == {
            "id": goal.id,
            "user": UserProfileSerializer(current_user_goal.user).data,
            "created":  timezone.localtime(goal.created).isoformat(),
            "updated": timezone.localtime(goal.updated).isoformat(),
            'title': 'Call home',
            "status": current_user_goal.status,
            "category": current_user_category.id,
            "description": "call home tomorrow",
            "priority": goal.priority,
            "due_date": timezone.localtime(goal.due_date).isoformat()
        }

    def test_goal_destroy_view(self, client, current_board_participant, current_user_goal):
        """Test for deleting a goal by current_board_participant with owner role"""

        client.force_login(user=current_board_participant.user)

        response = client.delete(
            path=f"/goals/goal/{current_user_goal.id}",
        )

        goal = Goal.objects.get(id=current_user_goal.id)

        assert response.status_code == 204
        assert goal.status == Status.archived

    def test_goal_retrieve_view_forbidden(self, client, current_user_goal):
        """Test for retrieving another user's goal without a role for the board"""

        other_user = UserFactory()
        client.force_login(user=other_user)

        response = client.get(path=f"/goals/goal/{current_user_goal.id}")

        assert response.status_code == 404

    def test_goal_update_view_reader(self, client, current_board_participant, current_user_goal):
        """Test for updating a goal by current_board_participant with reader role"""

        current_board_participant.role = BoardParticipant.Role.reader
        current_board_participant.save()

        client.force_login(user=current_board_participant.user)

        data = {'title': 'Business'}

        response = client.patch(
            path=f"/goals/goal/{current_user_goal.id}",
            data=data,
            content_type='application/json',
        )

        assert response.status_code == 403
        assert response.data == {
            'detail': ErrorDetail(
                string='У Вас нет права редактирования или удаления данной цели',
                code='permission_denied'
            )
        }

    def test_goal_destroy_view_writer(self, client, current_board_participant, current_user_goal):
        """Test for deleting a goal by current_board_participant with writer role"""

        current_board_participant.role = BoardParticipant.Role.writer
        current_board_participant.save()

        client.force_login(user=current_board_participant.user)

        response = client.delete(
            path=f"/goals/goal/{current_user_goal.id}",
        )

        goal = Goal.objects.get(id=current_user_goal.id)

        assert response.status_code == 204
        assert goal.status == Status.archived
