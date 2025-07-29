from django.db.models import Prefetch
from rest_framework import mixins
from rest_framework import viewsets

from timetable.core.api.serializers.audience_serializer import AudienceWithSubjectsSerializer
from timetable.core.models import Audience
from timetable.core.models import Subject


class AudienceViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    # Получение информации об аудитории и связанных с ней занятиях.

    ## Этот эндпоинт позволяет получить подробную информацию об одной аудитории
    ## по её ID, включая список занятий, которые проходят в этой аудитории.
    """

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
