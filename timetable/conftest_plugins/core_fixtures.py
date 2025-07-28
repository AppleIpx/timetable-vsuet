import pytest

from timetable.core.enums import EveryWeek
from timetable.core.test.factories.audience import AudienceFactory
from timetable.core.test.factories.subject import SubjectFactory


@pytest.fixture
def subject():
    """Фикстура по созданию предмета без повторений"""
    return SubjectFactory()


@pytest.fixture
def some_subjects(audience):
    """Фикстура по созданию нескольких предметов без повторения с конкретной аудиторией для всех предметов"""
    return SubjectFactory.create_batch(size=5, audience=audience)


@pytest.fixture
def subject_with_everyweek_repeat(audience):
    """Фикстура по созданию предмета с повторением каждую неделю с конкретной аудиторией для всех предметов"""
    return SubjectFactory.create_batch(5, audience=audience, rule_of_repeat=EveryWeek)


@pytest.fixture
def audience():
    """Фикстура по созданию аудитории"""
    return AudienceFactory()
