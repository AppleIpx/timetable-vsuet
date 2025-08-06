from datetime import datetime
from datetime import time

from django.db.models import Prefetch
from django.utils import timezone
from django.utils.timezone import make_aware
from pytz import utc
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
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
    """
    # API для получения расписания занятий.
    Позволяет:
    - Получить полное расписание занятий с возможностью фильтрации по дате, типу недели, группе и подгруппе.

    ## Доступные действия:
    - `GET /api/timetable/` — список всех занятий, с возможностью фильтрации.
    - `GET /api/timetable/me/` — персональное расписание для текущего пользователя. Требует авторизации.

    ## Фильтры для списка (`/api/timetable/`):
    - `date_min`: Дата начала или повторения после `включительно` (в формате `YYYY-MM-DD`).
    - `date_max`: Дата начала или повторения до `включительно` (в формате `YYYY-MM-DD`).
    - `type_of_week`: Тип недели (например, `Числитель` или `Знаменатель`).
    - `group__name`: Название группы (например, `У-123`).
    - `subgroup`: Номер подгруппы (1, 2 или 3).

        Логика фильтрации по подгруппам:
        - Если указана подгруппа 1, возвращаются предметы с подгруппой 1 и общей (3).
        - Если указана подгруппа 2, возвращаются предметы с подгруппой 2 и общей (3).
        - Если указана подгруппа 3 (общая), возвращаются только предметы с подгруппой 3.
    """

    serializer_class = SubjectSerializer
    filterset_class = SubjectFilter

    def get_queryset(self):
        base_queryset = (
            Subject.objects.select_related(
                "audience",
                "time_subject",
                "teacher",
                "group",
            )
            .order_by("date", "time_subject__start_time")
            .distinct()
        )

        repeat_dates_qs = self.get_filtered_repeat_dates()
        return base_queryset.prefetch_related(
            Prefetch("repeat_dates", queryset=repeat_dates_qs),
        )

    def get_filtered_repeat_dates(self):
        """
        Фильтрация повторяющихся дат в зависимости от query-параметров или действия `me`.
        """
        request = self.request
        action = getattr(self, "action", None)

        date_min = request.query_params.get("date_min")
        date_max = request.query_params.get("date_max")

        date_min_dt = self._parse_datetime(date_min, is_start=True) if date_min else None
        date_max_dt = self._parse_datetime(date_max, is_start=False) if date_max else None

        repeat_dates_qs = SubjectRepeat.objects.all()

        if action == "me":
            today = timezone.now().date()
            start_week, end_week = get_two_week_range(today)
            return repeat_dates_qs.filter(date__range=(start_week, end_week))

        if date_min_dt and date_max_dt:
            return repeat_dates_qs.filter(date__range=(date_min_dt, date_max_dt))
        if date_min_dt:
            return repeat_dates_qs.filter(date__gte=date_min_dt)
        if date_max_dt:
            return repeat_dates_qs.filter(date__lte=date_max_dt)

        return repeat_dates_qs

    def _parse_datetime(self, date_str: str, *, is_start: bool) -> datetime:
        """
        Парсит дату в datetime с учетом начала/конца дня и делает aware.
        """
        dt = datetime.fromisoformat(date_str).date()
        time_part = time.min if is_start else time.max
        return make_aware(datetime.combine(dt, time_part), timezone=utc)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def me(self, request: Request) -> Response:
        """
        # Возвращает персональное расписание авторизованного пользователя на текущую учебную неделю.

        ## Расписание включает:
        - Занятия, начинающиеся в пределах текущей недели.
        - Занятия, начавшиеся ранее, но имеющие повторения в текущей неделе.

        ## Логика зависит от роли пользователя:
        - Для студентов: отображаются занятия, на которых студент должен присутствовать.
        - Для преподавателей: отображаются занятия, которые преподаватель проводит.

        ### Период охватывает текущую неделю начиная с понедельника и заканчивая воскресеньем. Например, сегодня
        ### 16 июля(среда) и период будет включать в себя с 14 июля(понедельник) до 27 июля(воскресенье)

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
