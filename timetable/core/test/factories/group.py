import factory
from factory.django import DjangoModelFactory

from timetable.core.models import Group


class GroupFactory(DjangoModelFactory):
    class Meta:
        model = Group

    name = factory.Faker("word")
