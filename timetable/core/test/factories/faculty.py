import factory
from factory.django import DjangoModelFactory

from timetable.core.models import Faculty


class FacultyFactory(DjangoModelFactory):
    name = factory.Faker("name")

    class Meta:
        model = Faculty
