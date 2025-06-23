from factory import Faker
from factory.django import DjangoModelFactory

from timetable.core.models import Audience


class AudienceFactory(DjangoModelFactory):
    name = Faker("name")

    class Meta:
        model = Audience
