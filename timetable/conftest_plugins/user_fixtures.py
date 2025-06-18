import pytest

from timetable.users.models import User
from timetable.users.tests.factories import TeacherFactory
from timetable.users.tests.factories import UserFactory


@pytest.fixture
def teacher():
    return TeacherFactory()


@pytest.fixture
def user(db) -> User:
    return UserFactory()
