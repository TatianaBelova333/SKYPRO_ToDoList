import pytest
from django.utils import timezone
from core.serializers import UserProfileSerializer
from goals.models import GoalComment, BoardParticipant
from goals.serializers import GoalCommentSerializer


@pytest.mark.django_db
class TestCommentView:
    """BoardView tests suite"""

    def test_comment_detail_unauthorised(self, client, current_user_comment):
        """Test for retrieving one comment by unauthorised user"""

        response = client.get(path=f"/goals/goal_comment/{current_user_comment.id}")

        assert response.status_code == 401

    def test_comment_detail_view(self, client, current_board_participant, current_user_comment):
        """Test for retrieving a comment by authorised user with owner role"""

        client.force_login(user=current_board_participant.user)

        expected_response = GoalCommentSerializer(current_user_comment).data
        response = client.get(path=f"/goals/goal_comment/{current_user_comment.id}")

        assert response.status_code == 200
        assert response.data == expected_response

    def test_comment_update_view(self, client, current_board_participant, current_user_comment):
        """Test for retrieving and updating a board by authorised user with owner role"""

        client.force_login(user=current_board_participant.user)

        data = {'text': 'My Comment'}

        response = client.patch(
            path=f"/goals/goal_comment/{current_user_comment.id}",
            data=data,
            content_type='application/json',
        )
        comment = GoalComment.objects.latest('updated')

        assert response.status_code == 200
        assert response.data == {
            "id": current_user_comment.id,
            "user": UserProfileSerializer(current_user_comment.user).data,
            "created":  timezone.localtime(current_user_comment.created).isoformat(),
            "updated": timezone.localtime(comment.updated).isoformat(),
            "text": "My Comment",
            "goal": current_user_comment.goal.id
        }

    def test_comment_destroy_view(self, client, current_board_participant, current_user_comment):
        """Test for deleting a goal comment by authorised user with owner role"""

        client.force_login(user=current_board_participant.user)

        response = client.delete(
            path=f"/goals/goal_comment/{current_user_comment.id}",
        )

        comment_exists = GoalComment.objects.filter(id=current_user_comment.id).exists()

        assert response.status_code == 204
        assert comment_exists is False

    def test_comment_update_view_not_owner(self, client, current_board_participant, another_user_board, another_user_comment):
        """Test for retrieving and updating another user's comment by current user with writer role"""

        current_board_participant.board = another_user_board
        current_board_participant.role = BoardParticipant.Role.writer
        current_board_participant.save()

        client.force_login(user=current_board_participant.user)

        data = {'text': 'My Comment'}

        response = client.patch(
            path=f"/goals/goal_comment/{another_user_comment.id}",
            data=data,
            content_type='application/json',
        )
        comment = GoalComment.objects.get(id=another_user_comment.id)

        assert response.status_code == 404
        assert another_user_comment == comment

