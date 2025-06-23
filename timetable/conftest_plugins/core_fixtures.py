import pytest

from timetable.core.test.factories.subject import SubjectFactory


@pytest.fixture
def subject():
    return SubjectFactory()
