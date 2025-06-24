import pytest

from timetable.core.test.factories.audience import AudienceFactory
from timetable.core.test.factories.subject import SubjectFactory


@pytest.fixture
def subject():
    return SubjectFactory()


@pytest.fixture
def audience():
    return AudienceFactory()
