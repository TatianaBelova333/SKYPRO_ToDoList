import pytest
from django.urls import reverse
from goals.models import BoardParticipant
from goals.serializers import BoardSerializer


@pytest.mark.django_db
class TestBoardListView:
    """BoardListView test suite"""

    def test_board_list_owner(self, client, current_board_participant, current_user_boards):
        """Test for retrieving boards list for current user with owner role"""

        client.force_login(user=current_board_participant.user)
        response = client.get(path=reverse('goals:list_boards'))

        assert response.status_code == 200
        assert response.data == BoardSerializer(current_user_boards, many=True).data

    def test_board_list_writer(self, client, current_board_participant):
        """Board list retrieving test for current board participant with writer role"""

        current_board_participant.role = BoardParticipant.Role.writer
        current_board_participant.save()

        user = current_board_participant.user
        board = current_board_participant.board

        client.force_login(user=user)

        response = client.get(path=reverse('goals:list_boards'))

        assert response.status_code == 200
        assert response.data == [BoardSerializer(board).data]

    def test_board_list_reader(self, client, current_board_participant):
        """Board list retrieving for current board_participant with writer role"""

        current_board_participant.role = BoardParticipant.Role.reader
        current_board_participant.save()

        user = current_board_participant.user
        board = current_board_participant.board

        client.force_login(user=user)

        response = client.get(path=reverse('goals:list_boards'))

        assert response.status_code == 200
        assert response.data == [BoardSerializer(board).data]

    def test_board_list_deleted(self, client, board_participant):
        """Test for retrieving list of deleted boards"""

        board = board_participant.board
        board.is_deleted = True
        board.save()

        client.force_login(user=board_participant.user)

        response = client.get(path=reverse('goals:list_boards'))

        assert response.status_code == 200
        assert response.data == []

    def test_board_list_filter_by_limit_offset(self, client, current_board_participant, current_user_boards):
        """Boards list pagination test"""

        client.force_login(user=current_board_participant.user)
        limit = 3
        offset = 3
        boards = BoardSerializer(current_user_boards, many=True).data

        response = client.get(path=f"/goals/board/list?limit={limit}")
        assert response.status_code == 200
        assert response.data == {
            "count": len(boards),
            "next": f'http://testserver/goals/board/list?limit={limit}&offset={offset}',
            "previous": None,
            "results": boards[:limit],
        }
