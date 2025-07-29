import pytest

from timetable.users.models import User
from timetable.users.tests.factories import StudentFactory
from timetable.users.tests.factories import TeacherFactory
from timetable.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def _media_storage(settings, tmpdir) -> None:
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def teacher():
    return TeacherFactory()


@pytest.fixture
def student():
    return StudentFactory()


@pytest.fixture
def user(db) -> User:
    return UserFactory()
