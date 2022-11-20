import pytest
from goals.models import Goal, BoardParticipant, Board, GoalCategory

from tests.factories import UserFactory, CategoryFactory, BoardParticipantFactory, GoalFactory, \
    CommentFactory, BoardFactory


@pytest.fixture()
def current_user(user):
    return user


@pytest.fixture()
def current_board_participant(board_participant):
    return board_participant


@pytest.fixture()
def current_user_board(current_board_participant):
    board = current_board_participant.board
    return board


@pytest.fixture()
def current_user_category(current_board_participant):
    user_category = CategoryFactory(board=current_board_participant.board, user=current_board_participant.user)
    goal = GoalFactory(category=user_category, user=current_board_participant.user)

    return user_category


@pytest.fixture()
def current_user_goal(current_user_category, current_board_participant):
    goal = GoalFactory(category=current_user_category, user=current_board_participant.user)
    return goal


@pytest.fixture()
def current_user_goals(current_board_participant, current_user_category):
    """Generates """
    user = current_board_participant.user
    GoalFactory.create_batch(size=4, user=user, category=current_user_category)

    return Goal.objects.all()


@pytest.fixture()
def current_user_categories(board_participant):
     CategoryFactory.create_batch(
        size=4,
        user=board_participant.user,
        board=board_participant.board,
    )
     return GoalCategory.objects.all()


@pytest.fixture()
def current_user_boards(current_board_participant):
    """Creates boards for the current user with the owner role"""
    current_user = current_board_participant.user
    boards = BoardFactory.create_batch(size=4)

    for board in boards:
        BoardParticipantFactory(user=current_user, board=board)

    return Board.objects.all()


@pytest.fixture()
def goal_with_comments(current_board_participant, goal):
    """Generates comments for a goal and returns the goal"""

    current_user = current_board_participant.user

    another_board_participant = BoardParticipantFactory(
        user=UserFactory(first_name='Petr'),
        board=goal.category.board,
        role=BoardParticipant.Role.writer
    )
    another_user = another_board_participant.user

    current_user_comments = CommentFactory.create_batch(size=3, goal=goal, user=current_user)
    another_user_comments = CommentFactory.create_batch(size=3, goal=goal, user=another_user)

    return goal


@pytest.fixture()
def current_user_comment(current_board_participant):
    category = CategoryFactory(board=current_board_participant.board, user=current_board_participant.user)
    goal = GoalFactory(category=category, user=current_board_participant.user)
    comment = CommentFactory(goal=goal, user=current_board_participant.user)

    return comment


@pytest.fixture()
def another_user():
    another_user = UserFactory(first_name='John', last_name='Johnson')
    return another_user


@pytest.fixture()
def another_user_board():
    board = BoardFactory()
    return board


@pytest.fixture()
def another_board_participant(another_user, another_user_board):
    another_board_participant = BoardParticipantFactory(
        user=another_user,
        board=another_user,
        role=BoardParticipant.Role.owner
    )
    return another_board_participant


@pytest.fixture()
def another_user_category(another_user_board, another_user):
    another_user_category = CategoryFactory(board=another_user_board, user=another_user)
    return another_user_category


@pytest.fixture()
def another_user_goal(another_user, another_user_category):
    another_user_goal = GoalFactory(user=another_user, category=another_user_category)
    return another_user_goal


@pytest.fixture()
def another_user_comment(another_user, goal):
    another_user_comment = CommentFactory(goal=goal, user=another_user)
    return another_user_comment


@pytest.fixture()
def other_user_categories():
    other_user = UserFactory()
    other_board = BoardFactory()
    CategoryFactory.create_batch(size=4, user=other_user, board=other_board)
    return GoalCategory.objects.all()

