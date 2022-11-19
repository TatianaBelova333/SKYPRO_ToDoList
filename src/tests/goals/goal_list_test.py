import pytest
from django.urls import reverse
from rest_framework.exceptions import ErrorDetail
from goals.models import BoardParticipant, Status
from goals.serializers import GoalSerializer


@pytest.mark.django_db
class TestGoalListView:
    """GoalListView test suite"""

    def test_goal_list_success(self, client, current_board_participant, current_user_goals):
        """Test for retrieving goal list sorted by default (priority & due_date) for authorised board_participant"""

        client.force_login(user=current_board_participant.user)
        goals = current_user_goals.order_by('-priority', 'due_date')

        goals = GoalSerializer(goals, many=True).data

        response = client.get(path=reverse('goals:list_goals'))

        assert response.status_code == 200
        assert response.data == goals

    def test_goal_list_unauthorised(self, client):
        """Test for retrieving goal list for unauthorised user"""

        response = client.get(path=reverse('goals:list_goals'))

        assert response.status_code == 401
        assert response.data == {'detail': ErrorDetail(
            string='Authentication credentials were not provided.',
            code='not_authenticated')}

    def test_goal_list_sort_by_priority_or_due_date(self, client, current_board_participant, current_user_goals):
        """Test for retrieving goal list sorted by priority or due_date"""

        client.force_login(user=current_board_participant.user)

        goals_sorted_by_due_date = GoalSerializer(current_user_goals.order_by('due_date'), many=True).data
        goals_sorted_by_priority = GoalSerializer(current_user_goals.order_by('-priority', 'due_date'), many=True).data

        response_priority = client.get(path=f"/goals/goal/list?ordering=priority")
        response_due_date = client.get(path=f"/goals/goal/list?ordering=due_date")

        assert response_priority.status_code == 200
        assert response_due_date.status_code == 200
        assert response_priority.data == goals_sorted_by_priority
        assert response_due_date.data == goals_sorted_by_due_date

    def test_goal_list_reader(self, client, current_board_participant, current_user_goals):
        """Test for retrieving goal list for board_participant with reader role"""

        current_board_participant.role = BoardParticipant.Role.reader
        current_board_participant.save()

        user = current_board_participant.user
        client.force_login(user=user)

        response = client.get(path=reverse('goals:list_goals'))
        goals = current_user_goals.order_by('-priority', 'due_date')

        goals = GoalSerializer(goals, many=True).data

        assert response.status_code == 200
        assert response.data == goals

    def test_goal_list_writer(self, client, current_board_participant, current_user_goals):
        """Test for retrieving goal list for board_participant with writer role"""

        current_board_participant.role = BoardParticipant.Role.writer
        current_board_participant.save()

        client.force_login(user=current_board_participant.user)

        response = client.get(path=reverse('goals:list_goals'))
        goals = current_user_goals.order_by('-priority', 'due_date')

        goals = GoalSerializer(goals, many=True).data

        assert response.status_code == 200
        assert response.data == goals

    def test_goal_list_search_by_title(self, client, current_board_participant, current_user_goals):
        """Test for searching goals by title"""

        client.force_login(user=current_board_participant.user)

        query1 = "Test"
        query2 = "Goal"
        query3 = "test"
        query4 = 'dog'

        for query in [query1, query2, query3, query4]:
            response = client.get(path=f"/goals/goal/list?search={query}")
            all_goals = current_user_goals.filter(title__icontains=query).order_by('-priority', 'due_date')
            all_goals = GoalSerializer(all_goals, many=True).data
            assert response.status_code == 200
            assert response.data == all_goals

    def test_goal_list_archived_status(self, client, current_board_participant, current_user_goals):
        """Test for retrieving goal list with archived status"""

        current_user_goals.update(status=Status.archived)

        client.force_login(user=current_board_participant.user)

        response = client.get(path=reverse('goals:list_goals'))

        assert response.status_code == 200
        assert response.data == []

    def test_goal_list_filter_by_status(self, client, current_board_participant, current_user_goals):
        """Test for retrieving goal list filtered by status"""

        client.force_login(user=current_board_participant.user)

        status_queries = ['1', '1,2', '1,2,3']

        for query in status_queries:
            response = client.get(path=f"/goals/goal/list?status__in={query}")
            all_goals = current_user_goals.filter(status__in=query.split(',')).order_by('-priority', 'due_date')
            all_goals = GoalSerializer(all_goals, many=True).data
            assert response.status_code == 200
            assert response.data == all_goals

    def test_goal_list_filter_by_priority(self, client, current_board_participant, current_user_goals):
        """Test for retrieving goal list filtered by priority"""

        client.force_login(user=current_board_participant.user)

        priority_queries = ['1', '1,2', '1,2,3']
        for query in priority_queries:
            response = client.get(path=f"/goals/goal/list?priority__in={query}")
            all_goals = current_user_goals.filter(priority__in=query.split(',')).order_by('-priority', 'due_date')
            all_goals = GoalSerializer(all_goals, many=True).data

            assert response.status_code == 200
            assert response.data == all_goals

    def test_goal_list_several_filters(self, client, current_board_participant, current_user_goals):
        """Test for retrieving goal list filtered by mixed filters"""

        user = current_board_participant.user
        client.force_login(user=user)

        priority = '1,2'
        status = '1,2,3'

        response = client.get(
            path=f"/goals/goal/list?priority__in={priority}&status__in={status}"
        )

        goals = current_user_goals.filter(priority__in=priority.split(','), status__in=status.split(',')).\
            order_by('-priority', 'due_date')

        expected_result = GoalSerializer(goals, many=True).data

        assert response.status_code == 200
        assert response.data == expected_result
