import factory
from factory import fuzzy
from factory.django import DjangoModelFactory

from timetable.core.enums import TYPE_OF_CLASSES_CHOICES
from timetable.core.enums import TYPE_OF_WEEK_CHOICES
from timetable.core.enums import WITHOUT_REPETITION
from timetable.core.models import Subject
from timetable.core.test.factories.audience import AudienceFactory
from timetable.core.test.factories.group import GroupFactory
from timetable.core.test.factories.time_subject import TimeSubjectFactory
from timetable.users.tests.factories import TeacherFactory


class SubjectFactory(DjangoModelFactory):
    """Фабрика по созданию предмета, без повторения."""

    class Meta:
        model = Subject

    name = factory.Faker("sentence", nb_words=3)
    audience = factory.SubFactory(AudienceFactory)
    rule_of_repeat = WITHOUT_REPETITION
    type_of_week = factory.LazyFunction(
        lambda: fuzzy.FuzzyChoice([choice[0] for choice in TYPE_OF_WEEK_CHOICES]).fuzz(),
    )
    type_of_classes = factory.LazyFunction(
        lambda: fuzzy.FuzzyChoice([choice[0] for choice in TYPE_OF_CLASSES_CHOICES]).fuzz(),
    )
    time_subject = factory.SubFactory(TimeSubjectFactory)
    teacher = factory.SubFactory(TeacherFactory)
    group = factory.SubFactory(GroupFactory)
    subgroup = fuzzy.FuzzyInteger(1, 2)
