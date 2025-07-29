from django.db.models import Prefetch
from django.utils import timezone
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from timetable.core.api.serializers.list_subject_serializer import SubjectMeSerializer
from timetable.core.api.serializers.list_subject_serializer import SubjectSerializer
from timetable.core.api.utils import get_two_week_range
from timetable.core.filters.subject_filters import SubjectFilter
from timetable.core.models import Subject
from timetable.core.models import SubjectRepeat
from timetable.core.service.subject_my_service import MySubjectService


class TimetableViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = SubjectSerializer
    filterset_class = SubjectFilter

    def get_queryset(self):
        queryset = (
            Subject.objects.select_related(
                "audience",
                "time_subject",
                "teacher",
                "group",
            )
            .order_by("date")
            .distinct()
        )

        action = getattr(self, "action", None)

        repeat_dates_qs = SubjectRepeat.objects.all()

        if action == "me":
            current_time = timezone.now().date()
            start_week, end_week = get_two_week_range(current_time)
            repeat_dates_qs = repeat_dates_qs.filter(date__range=(start_week, end_week))

        return queryset.prefetch_related(Prefetch("repeat_dates", queryset=repeat_dates_qs))

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def me(self, request: Request) -> Response:
        """
        Возвращает расписание для авторизованного пользователя с начала и до конца недели,
        включая те предметы, которые начались раньше, но имеют повторения на этой неделе.
        """
        user = request.user
        current_time = timezone.now().date()

        service = MySubjectService(self.get_queryset(), current_time=current_time, user=user)
        subjects = service()

        serializer = SubjectMeSerializer(
            subjects,
            many=True,
            context={
                "request": request,
                "start_weekday": service.start_weekday,
                "end_weekday": service.end_weekday,
            },
        )
        return Response(serializer.data)
