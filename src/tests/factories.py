from datetime import datetime
from dateutil.tz import UTC
from django.utils import timezone
import factory.fuzzy
from core.models import User
from goals.models import Board, GoalCategory, BoardParticipant, Goal, Status, Priority, GoalComment


class UserFactory(factory.django.DjangoModelFactory):
    """Test class for User Class"""

    class Meta:
        model = User

    first_name = "Vasily"
    last_name = "Ivanov"
    username = factory.Sequence(lambda n: 'user%d' % n)


class BoardFactory(factory.django.DjangoModelFactory):
    """Test class for Board class"""

    class Meta:
        model = Board

    title = factory.fuzzy.FuzzyText(length=15)
    is_deleted = False
    created = timezone.now()
    updated = timezone.now()


class CategoryFactory(factory.django.DjangoModelFactory):
    """Test class for GoalCategory class"""

    class Meta:
        model = GoalCategory

    title = factory.fuzzy.FuzzyText(length=15)
    is_deleted = False
    created = factory.fuzzy.FuzzyDateTime(datetime(2008, 1, 1, tzinfo=UTC), datetime(2023, 1, 1, tzinfo=UTC))
    updated = factory.fuzzy.FuzzyDateTime(datetime(2008, 1, 1, tzinfo=UTC), datetime(2023, 1, 1, tzinfo=UTC))
    user = factory.SubFactory(UserFactory)
    board = factory.SubFactory(BoardFactory)


class BoardParticipantFactory(factory.django.DjangoModelFactory):
    """Test class for BoardParticipant class"""

    class Meta:
        model = BoardParticipant

    user = factory.SubFactory(UserFactory)
    board = factory.SubFactory(BoardFactory)
    role = BoardParticipant.Role.owner


class GoalFactory(factory.django.DjangoModelFactory):
    """Test class for Goal class"""

    class Meta:
        model = Goal

    user = factory.SubFactory(UserFactory)
    title = factory.fuzzy.FuzzyText(length=15, prefix='test', suffix='goal')
    description = 'test'
    due_date = factory.fuzzy.FuzzyDateTime(datetime(2022, 1, 1, tzinfo=UTC), datetime(2023, 1, 1, tzinfo=UTC))
    status = factory.fuzzy.FuzzyChoice([Status.to_do, Status.in_progress, Status.done])
    priority = factory.fuzzy.FuzzyChoice([Priority.critical, Priority.low, Priority.medium, Priority.high])
    category = factory.SubFactory(CategoryFactory)
    created = factory.fuzzy.FuzzyDateTime(datetime(2008, 1, 1, tzinfo=UTC), datetime(2023, 1, 1, tzinfo=UTC))
    updated = factory.fuzzy.FuzzyDateTime(datetime(2008, 1, 1, tzinfo=UTC), datetime(2023, 1, 1, tzinfo=UTC))


class CommentFactory(factory.django.DjangoModelFactory):
    """Test class for GoalComment class"""

    class Meta:
        model = GoalComment

    text = factory.fuzzy.FuzzyText(length=15)
    user = factory.SubFactory(UserFactory)
    goal = factory.SubFactory(GoalFactory)
    created = factory.fuzzy.FuzzyDateTime(datetime(2008, 1, 1, tzinfo=UTC), datetime(2023, 1, 1, tzinfo=UTC))
    updated = factory.fuzzy.FuzzyDateTime(datetime(2008, 1, 1, tzinfo=UTC), datetime(2023, 1, 1, tzinfo=UTC))
