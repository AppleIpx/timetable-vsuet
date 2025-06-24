import factory
from factory.django import DjangoModelFactory

from timetable.core.models import TimeSubject


class TimeSubjectFactory(DjangoModelFactory):
    class Meta:
        model = TimeSubject

    number = factory.Sequence(lambda n: n + 10)
    start_time = factory.Faker("time_object")
    end_time = factory.Faker("time_object")
