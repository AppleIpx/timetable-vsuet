import secrets

import factory
from factory.django import DjangoModelFactory

from timetable.core.models import TimeSubject


class TimeSubjectFactory(DjangoModelFactory):
    class Meta:
        model = TimeSubject

    number = factory.LazyFunction(lambda: secrets.randbelow(100) + 1)
    start_time = factory.Faker("time_object")
    end_time = factory.Faker("time_object")
