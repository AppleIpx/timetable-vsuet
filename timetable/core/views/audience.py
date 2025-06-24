from django.db.models import Prefetch
from rest_framework import mixins
from rest_framework import viewsets

from timetable.core.models import Audience
from timetable.core.models import Subject
from timetable.core.serializers.audience_serializer import AudienceWithSubjectsSerializer


class AudienceViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = AudienceWithSubjectsSerializer
    queryset = Audience.objects.prefetch_related(
        Prefetch(
            "subject_set",
            queryset=Subject.objects.select_related(
                "time_subject",
                "teacher",
                "group",
            ),
        ),
    )
