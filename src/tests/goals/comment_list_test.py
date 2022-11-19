import pytest
from django.urls import reverse
from rest_framework.exceptions import ErrorDetail
from goals.models import BoardParticipant
from goals.serializers import GoalCommentSerializer


@pytest.mark.django_db
class TestGoalCommentListView:
    """GoalCommentListView test suite"""

    def test_comment_list_success(self, client, current_board_participant, goal_with_comments):
        """Test for goal comments list sorted by default field (created) for authorised board_participant"""

        client.force_login(user=current_board_participant.user)

        comments = GoalCommentSerializer(goal_with_comments.comments.order_by('-created'), many=True).data
        response = client.get(path=f'/goals/goal_comment/list?goal={goal_with_comments.id}')

        assert response.status_code == 200
        assert response.data == comments

    def test_goal_list_unauthorised(self, client):
        """Test for retrieving goal list for unauthorised user"""

        response = client.get(path=reverse('goals:list_comments'))

        assert response.status_code == 401
        assert response.data == {'detail': ErrorDetail(
            string='Authentication credentials were not provided.',
            code='not_authenticated')}

    def test_goal_list_reader(self, client, current_board_participant, goal_with_comments):
        """Test for retrieving goal comments for board_participant with reader role"""

        current_board_participant.role = BoardParticipant.Role.reader
        current_board_participant.save()

        client.force_login(user=current_board_participant.user)
        current_board_participant.save()

        comments = GoalCommentSerializer(goal_with_comments.comments.order_by('-created'), many=True).data
        response = client.get(path=f'/goals/goal_comment/list?goal={goal_with_comments.id}')

        assert response.status_code == 200
        assert response.data == comments

    def test_goal_list_writer(self, client, current_board_participant, goal_with_comments):
        """Test for retrieving goal comments for board_participant with writer role"""

        current_board_participant.role = BoardParticipant.Role.writer
        current_board_participant.save()

        client.force_login(user=current_board_participant.user)
        current_board_participant.save()

        comments = GoalCommentSerializer(goal_with_comments.comments.order_by('-created'), many=True).data
        response = client.get(path=f'/goals/goal_comment/list?goal={goal_with_comments.id}')

        assert response.status_code == 200
        assert response.data == comments

    def test_goal_list_sort_by_updated_created(self, client, current_board_participant, goal_with_comments):
        """Test for sorting goal comments list by created and updated fields """

        client.force_login(user=current_board_participant.user)

        response_created = client.get(
            path=f"/goals/goal_comment/list?orderField=created&ordering=created&goal={goal_with_comments.id}"
        )
        response_updated = client.get(
            path=f"/goals/goal_comment/list?orderField=created&ordering=updated&goal={goal_with_comments.id}"
        )
        comments_by_created = GoalCommentSerializer(goal_with_comments.comments.order_by('created'), many=True).data
        comments_by_updated = GoalCommentSerializer(goal_with_comments.comments.order_by('updated'), many=True).data

        assert response_created.status_code == 200
        assert response_created.data == comments_by_created
        assert response_updated.status_code == 200
        assert response_updated.data == comments_by_updated
