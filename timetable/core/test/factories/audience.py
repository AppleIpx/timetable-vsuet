from factory import Faker
from factory.django import DjangoModelFactory

from timetable.core.models import Audience


class AudienceFactory(DjangoModelFactory):
    name = Faker("word")

    class Meta:
        model = Audience
