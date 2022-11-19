import pytest
from rest_framework.exceptions import ErrorDetail
from goals.models import Board, GoalCategory, Goal, Status, BoardParticipant
from goals.serializers import BoardSerializer


@pytest.mark.django_db
class TestBoardView:
    """BoardView tests suite"""

    def test_board_detail_unauthorised(self, client, current_board_participant):
        """Test for retrieving one board by unauthorised user"""

        board = current_board_participant.board

        response = client.get(path=f"/goals/board/{board.id}")

        assert response.status_code == 401

    def test_board_detail_view(self, client, current_board_participant):
        """Test for retrieving a board by authorised user with owner role"""

        client.force_login(user=current_board_participant.user)
        board = current_board_participant.board

        expected_response = BoardSerializer(board).data

        response = client.get(path=f"/goals/board/{board.id}")

        assert response.status_code == 200
        assert response.data == expected_response

    def test_board_destroy_view(self, client, current_board_participant, current_user_category):
        """Test for deleting a board by authorised user with owner role"""

        client.force_login(user=current_board_participant.user)
        board = current_board_participant.board

        response = client.delete(
            path=f"/goals/board/{board.id}",
        )

        deleted_board = Board.objects.latest('updated')
        category = GoalCategory.objects.get(id=current_user_category.id)
        goal = Goal.objects.get(category=current_user_category)

        assert response.status_code == 204
        assert deleted_board.is_deleted is True
        assert category.is_deleted is True
        assert goal.status == Status.archived

    def test_board_retrieve_view_forbidden(self, client, current_board_participant, another_user_board):
        """Test for retrieving another user's board"""

        client.force_login(user=current_board_participant.user)

        response = client.get(path=f"/goals/board/{another_user_board.id}")

        assert response.status_code == 404

    def test_board_update_view_reader(self, client, current_board_participant):
        """Test for updating a goal category by authorised user with reader role"""

        current_board_participant.role = BoardParticipant.Role.reader
        current_board_participant.save()

        client.force_login(user=current_board_participant.user)
        board = current_board_participant.board

        data = {'title': 'Business Board'}

        response = client.patch(
            path=f"/goals/board/{board.id}",
            data=data,
            content_type='application/json',
        )

        assert response.status_code == 403
        assert response.data == {
            'detail': ErrorDetail(string='У Вас нет права редактирования или удаления данной доски',
                                  code='permission_denied')
        }

    def test_board_destroy_view_writer(self, client, current_board_participant):
        """Test for deleting a board by authorised board participant with writer role"""

        current_board_participant.role = BoardParticipant.Role.writer
        current_board_participant.save()

        client.force_login(user=current_board_participant.user)
        board = current_board_participant.board

        response = client.delete(
            path=f"/goals/board/{board.id}",
        )
        board = Board.objects.get(id=board.id)

        assert response.status_code == 403
        assert board.is_deleted is False
        assert response.data == {
            'detail': ErrorDetail(string='У Вас нет права редактирования или удаления данной доски',
                                  code='permission_denied')
        }
