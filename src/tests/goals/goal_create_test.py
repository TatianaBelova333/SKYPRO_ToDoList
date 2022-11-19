import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework.exceptions import ErrorDetail

from core.models import User
from goals.models import Goal, GoalCategory, BoardParticipant


@pytest.mark.django_db
class TestGoalCreate:
    """GoalCreateView test suite"""

    def test_create_goal_success(self, client, current_board_participant, goal_category):
        """Goal creation test for current_board_participant with owner role"""
        user = current_board_participant.user
        client.force_login(user=user)

        data = {
            "title": "Do homework",
            "description": "Do homework",
            "category": goal_category.id,
        }

        response = client.post(
            path=reverse('goals:create_goal'),
            data=data,
            content_type='application/json',
        )

        goal = Goal.objects.last()

        assert response.status_code == 201
        assert response.data == {
            "id": goal.id,
            "status": 1,
            "title": "Do homework",
            "description": "Do homework",
            "due_date": None,
            "category": goal_category.id,
            "priority": 2,
            "created": timezone.localtime(goal.created).isoformat(),
            "updated": timezone.localtime(goal.updated).isoformat(),
        }

    def test_create_goal_unauthorized(self, client, goal_category):
        """Goal creation test for unauthorised user"""

        data = {
            "title": "Do homework",
            "description": "Do homework",
            "category": goal_category.id,
        }

        response = client.post(
            path=reverse('goals:create_goal'),
            data=data,
            content_type='application/json',
        )

        assert response.status_code == 401
        assert response.data == {
            'detail': ErrorDetail(string='Authentication credentials were not provided.', code='not_authenticated')
        }

    def test_create_goal_for_archived_category(self, client, current_board_participant, goal_category):
        """Goal creation test for archived category"""

        client.force_login(user=current_board_participant.user)
        goal_category.is_deleted = True
        goal_category.save()

        data = {
            "title": "Do homework",
            "description": "Do homework",
            "category": goal_category.id,
        }

        response = client.post(
            path=reverse('goals:create_goal'),
            data=data,
            content_type='application/json',
        )

        assert response.status_code == 400
        assert response.data == {'category': [ErrorDetail(string='Not allowed in deleted category', code='invalid')]}

    def test_create_goal_reader_role(self, client, current_board_participant, goal_category):
        """Goal creation test for current_board_participant with reader role"""

        current_board_participant.user = User.objects.create(username='david', password='qwerty123')
        current_board_participant.role = BoardParticipant.Role.reader
        current_board_participant.save()

        client.force_login(user=current_board_participant.user)

        data = {
            "title": "Do homework",
            "description": "Do homework",
            "category": goal_category.id,
        }

        response = client.post(
            path=reverse('goals:create_goal'),
            data=data,
            content_type='application/json',
        )

        assert response.status_code == 403
        assert response.data == {'detail': ErrorDetail(
            string='У Вас нет права создавать цели для данной категории.',
            code='permission_denied')
        }

    def test_create_goal_writer_role(self, client, current_board_participant, goal_category):
        """Goal creation test for current_board_participant with writer role"""

        current_board_participant.role = BoardParticipant.Role.writer
        current_board_participant.save()

        client.force_login(user=current_board_participant.user)

        data = {
            "title": "Do homework",
            "description": "Do homework",
            "category": goal_category.id,
        }

        response = client.post(
            path=reverse('goals:create_goal'),
            data=data,
            content_type='application/json',
        )

        goal = Goal.objects.last()

        assert response.status_code == 201
        assert response.data == {
            "id": goal.id,
            "status": 1,
            "title": "Do homework",
            "description": "Do homework",
            "due_date": None,
            "category": goal_category.id,
            "priority": 2,
            "created": timezone.localtime(goal.created).isoformat(),
            "updated": timezone.localtime(goal.updated).isoformat(),
        }
