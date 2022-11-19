import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework.exceptions import ErrorDetail
from goals.models import GoalCategory, BoardParticipant


@pytest.mark.django_db
class TestGoalCategoryCreateView:
    """GoalCategoryCreateView tests"""

    def test_create_category_unauthorised(self, client, board):
        """Goal category creation for unauthorised user"""
        expected_response = {
            'detail': ErrorDetail(string='Authentication credentials were not provided.', code='not_authenticated')
        }

        data = {
            "title": "Business",
            "board": board.id,
        }
        response = client.post(
            path=reverse('goals:create_category'),
            data=data,
            content_type='application/json',
        )
        assert response.data == expected_response
        assert response.status_code == 401

    def test_create_category_success(self, client, board_participant):
        """Goal category creation for authorised user with owner role"""
        user = board_participant.user
        board = board_participant.board
        client.force_login(user=user)

        data = {
            "title": "Business",
            "board": board.id,
        }
        response = client.post(
            path=reverse('goals:create_category'),
            data=data,
            content_type='application/json',
        )
        category = GoalCategory.objects.last()

        assert response.status_code == 201
        assert response.data == {
            "id": category.id,
            "created": timezone.localtime(category.created).isoformat(),
            "updated": timezone.localtime(category.updated).isoformat(),
            "title": "Business",
            "is_deleted": False,
            "board": board.id,
        }

    def test_create_category_for_archived_board(self, client, board_participant):
        """Goal category creation for deleted board"""

        client.force_login(user=board_participant.user)
        board = board_participant.board
        board.is_deleted = True
        board.save()

        data = {
            "title": "Business",
            "board": board.id,
        }
        response = client.post(
            path=reverse('goals:create_category'),
            data=data,
            content_type='application/json',
        )

        assert response.status_code == 400
        assert response.data == {'board': [ErrorDetail(string='Not allowed in deleted board', code='invalid')]}

    def test_create_category_reader_role(self, client, board_participant):
        """Goal category creation for user with reader role"""

        board_participant.role = BoardParticipant.Role.reader
        board_participant.save()

        client.force_login(user=board_participant.user)

        data = {
            "title": "Business",
            "board": board_participant.board.id,
        }
        response = client.post(
            path=reverse('goals:create_category'),
            data=data,
            content_type='application/json',
        )

        assert response.status_code == 403
        assert response.data == {'detail': ErrorDetail(
            string='У Вас нет права создавать категорию для данной доски.',
            code='permission_denied')
        }

    def test_create_category_writer_role(self, client, board_participant):
        """Goal category creation for user with writer role"""

        board_participant.role = BoardParticipant.Role.writer
        board_participant.save()

        client.force_login(user=board_participant.user)

        data = {
            "title": "Business",
            "board": board_participant.board.id,
        }
        response = client.post(
            path=reverse('goals:create_category'),
            data=data,
            content_type='application/json',
        )

        category = GoalCategory.objects.last()

        assert response.status_code == 201
        assert response.data == {
            "id": category.id,
            "created": timezone.localtime(category.created).isoformat(),
            "updated": timezone.localtime(category.updated).isoformat(),
            "title": "Business",
            "is_deleted": False,
            "board": board_participant.board.id,
        }
