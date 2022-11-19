import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework.exceptions import ErrorDetail
from goals.models import Board


@pytest.mark.django_db
class TestBoardCreateView:
    """BoardCreateView tests"""

    def test_create_board_unauthorised(self, client):
        """Test board creation for unauthorised users"""
        expected_response = {
            'detail': ErrorDetail(string='Authentication credentials were not provided.', code='not_authenticated')
        }

        data = {
            "title": "My Board",
        }
        response = client.post(
            data=data,
            path=reverse('goals:create_board'),
            content_type='application/json',
        )
        assert response.data == expected_response
        assert response.status_code == 401

    def test_create_board_success(self, client, current_user):
        """Board creation test for authorised current user"""

        client.force_login(user=current_user)

        data = {
            "title": "My Board",
        }
        response = client.post(
            data=data,
            path=reverse('goals:create_board'),
            content_type='application/json',
        )
        board = Board.objects.last()

        assert response.status_code == 201
        assert response.data == {
            "id": board.id,
            "created": timezone.localtime(board.created).isoformat(),
            "updated": timezone.localtime(board.updated).isoformat(),
            "title": "My Board",
            "is_deleted": False,
        }
