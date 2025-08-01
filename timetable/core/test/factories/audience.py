import factory
from factory.django import DjangoModelFactory

from timetable.core.models import Audience


class AudienceFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Аудитория-{n}")

    class Meta:
        model = Audience
