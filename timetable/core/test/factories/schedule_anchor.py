from factory.django import DjangoModelFactory

from timetable.core.models import ScheduleAnchor


class ScheduleAnchorFactory(DjangoModelFactory):
    class Meta:
        model = ScheduleAnchor
