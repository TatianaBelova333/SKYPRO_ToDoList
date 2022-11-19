import pytest
from django.urls import reverse
from rest_framework.exceptions import ErrorDetail
from goals.models import BoardParticipant
from goals.serializers import GoalCategorySerializer


@pytest.mark.django_db
class TestGoalCategoryListView:
    """GoalCategoryListView tests"""

    def test_category_list_success(self, client, current_board_participant, current_user_categories):
        """Test for goal category list retrieving for board_participant with owner role"""

        client.force_login(user=current_board_participant.user)

        response = client.get(path=reverse('goals:list_categories'))
        categories = current_user_categories.order_by('title')

        assert response.status_code == 200
        assert response.data == GoalCategorySerializer(categories, many=True).data

    def test_category_list_unauthorised(self, client):
        """Test for goal category list retrieving for unauthorised user"""

        response = client.get(path=reverse('goals:list_categories'))

        assert response.status_code == 401
        assert response.data == {'detail': ErrorDetail(
            string='Authentication credentials were not provided.',
            code='not_authenticated')}

    def test_category_list_forbidden(self, client, current_board_participant, other_user_categories):
        """Goal category test for user with forbidden access to board categories"""

        current_user = current_board_participant.user
        client.force_login(user=current_user)

        response = client.get(path=reverse('goals:list_categories'))

        assert response.status_code == 200
        assert response.data == []

    def test_category_list_reader(self, client, current_board_participant, current_user_categories):
        """Goal category list test for board_participant with reader role"""

        current_board_participant.role = BoardParticipant.Role.reader
        current_board_participant.save()

        client.force_login(user=current_board_participant.user)

        response = client.get(path=reverse('goals:list_categories'))
        goals = current_user_categories.order_by('title')

        assert response.status_code == 200
        assert response.data == GoalCategorySerializer(goals, many=True).data

    def test_category_list_writer(self, client, current_board_participant, current_user_categories):
        """Goal category list test for board_participant with writer role"""

        current_board_participant.role = BoardParticipant.Role.writer
        current_board_participant.save()

        client.force_login(user=current_board_participant.user)

        response = client.get(path=reverse('goals:list_categories'))
        goals = current_user_categories.order_by('title')

        assert response.status_code == 200
        assert response.data == GoalCategorySerializer(goals, many=True).data

    def test_category_list_filter_by_board(self, client, current_board_participant, current_user_categories):
        """Test for filtering goal category by board"""

        board = current_board_participant.board

        client.force_login(user=current_board_participant.user)

        response = client.get(path=f"/goals/goal_category/list?board={board.id}")
        goals = current_user_categories.order_by('title')

        assert response.status_code == 200
        assert response.data == GoalCategorySerializer(goals, many=True).data

    def test_category_list_search_by_title(self, client, current_board_participant, current_user_categories):
        """Test for searching goal categories by title"""

        client.force_login(user=current_board_participant.user)

        query1 = "Test"
        query2 = "Cat"
        query3 = "test"
        query4 = 'dog'

        for query in [query1, query2, query3, query4]:
            response = client.get(path=f"/goals/goal_category/list?search={query}")
            categories = current_user_categories.filter(title__icontains=query).order_by('title')
            assert response.status_code == 200
            assert response.data == GoalCategorySerializer(categories, many=True).data
