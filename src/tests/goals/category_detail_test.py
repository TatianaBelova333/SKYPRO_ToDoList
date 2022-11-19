import pytest
from django.utils import timezone
from rest_framework.exceptions import ErrorDetail
from core.serializers import UserProfileSerializer
from goals.models import GoalCategory, Status, Goal, BoardParticipant
from goals.serializers import GoalCategorySerializer
from tests.factories import UserFactory


@pytest.mark.django_db
class TestGoalCategoryView:
    """GoalCategoryView tests suite"""

    def test_category_detail_unauthorised(self, client, current_user_category):
        """Test for retrieving one goal category by unauthorised user"""

        response = client.get(path=f"/goals/goal_category/{current_user_category.id}")

        assert response.status_code == 401

    def test_category_retrieve_view(self, client, current_board_participant, current_user_category):
        """Test for retrieving a goal category by authorised user"""

        client.force_login(user=current_board_participant.user)

        expected_response = GoalCategorySerializer(current_user_category).data

        response = client.get(path=f"/goals/goal_category/{current_user_category.id}")

        assert response.status_code == 200
        assert response.data == expected_response

    def test_category_update_view(self, client, current_board_participant, current_user_category):
        """Test for retrieving and updating a goal category by authorised user"""

        client.force_login(user=current_board_participant.user)

        data = {'title': 'Business'}

        response = client.patch(
            path=f"/goals/goal_category/{current_user_category.id}",
            data=data,
            content_type='application/json',
        )
        category = GoalCategory.objects.latest('updated')

        assert response.status_code == 200
        assert response.data == {
            "id": category.id,
            "user": UserProfileSerializer(current_user_category.user).data,
            "created":  timezone.localtime(category.created).isoformat(),
            "updated": timezone.localtime(category.updated).isoformat(),
            "title": "Business",
            "is_deleted": current_user_category.is_deleted,
            "board": current_user_category.board.id
        }

    def test_category_destroy_view(self, client, current_board_participant, current_user_category):
        """Test for deleting a goal category by authorised user with owner role"""

        client.force_login(user=current_board_participant.user)

        response = client.delete(
            path=f"/goals/goal_category/{current_user_category.id}",
        )

        category = GoalCategory.objects.latest('updated')
        goal = Goal.objects.get(category=category)

        assert response.status_code == 204
        assert category.is_deleted is True
        assert goal.status == Status.archived

    def test_category_retrieve_view_forbidden(self, client, current_user_category):
        """Test for retrieving goal category by authorised user"""

        other_user = UserFactory()
        client.force_login(user=other_user)

        response = client.get(path=f"/goals/goal_category/{current_user_category.id}")

        assert response.status_code == 404

    def test_category_update_view_reader(self, client, current_board_participant, current_user_category):
        """Test for updating a goal category by authorised user with reader role"""

        current_board_participant.role = BoardParticipant.Role.reader
        current_board_participant.save()

        client.force_login(user=current_board_participant.user)

        data = {'title': 'Business'}

        response = client.patch(
            path=f"/goals/goal_category/{current_user_category.id}",
            data=data,
            content_type='application/json',
        )

        assert response.status_code == 403
        assert response.data == {
            'detail': ErrorDetail(string='У Вас нет права редактирования или удаления данной категории',
                                  code='permission_denied')
        }

    def test_category_destroy_view_writer(self, client, current_board_participant, current_user_category):
        """Test for deleting a goal category by authorised user with writer role"""

        current_board_participant.role = BoardParticipant.Role.writer
        current_board_participant.save()

        client.force_login(user=current_board_participant.user)

        response = client.delete(
            path=f"/goals/goal_category/{current_user_category.id}",
        )

        category = GoalCategory.objects.latest('updated')
        goal = Goal.objects.get(category=category)

        assert response.status_code == 204
        assert category.is_deleted is True
        assert goal.status == Status.archived
