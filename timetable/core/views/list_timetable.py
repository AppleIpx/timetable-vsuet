from rest_framework import mixins
from rest_framework import viewsets

from timetable.core.models import Subject
from timetable.core.serializers.list_subject_serializer import SubjectSerializer


class TimetableViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    filterset_fields = {
        "type_of_week": ["exact"],
        "group__name": ["exact"],
        "type_of_day": ["exact"],
        "subgroup": ["exact"],
    }
