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
    """
    # API для получения расписания занятий.
    Позволяет:
    - Получить полное расписание занятий с возможностью фильтрации по дате, типу недели, группе и подгруппе.

    ## Доступные действия:
    - `GET /api/timetable/` — список всех занятий, с возможностью фильтрации.
    - `GET /api/timetable/me/` — персональное расписание для текущего пользователя. Требует авторизации.

    ## Фильтры для списка (`/api/timetable/`):
    - `date_min`: Дата начала или повторения после (в формате `YYYY-MM-DD`).
    - `date_max`: Дата начала или повторения до (в формате `YYYY-MM-DD`).
    - `type_of_week`: Тип недели (например, `Числитель` или `Знаменатель`).
    - `group__name`: Название группы (например, `У-123`).
    - `subgroup`: Номер подгруппы (1, 2 или 3).

        Логика фильтрации по подгруппам:
        - Если указана подгруппа 1, возвращаются предметы с подгруппой 1 и общей (3).
        - Если указана подгруппа 2, возвращаются предметы с подгруппой 2 и общей (3).
        - Если указана подгруппа 3 (общая), возвращаются только предметы с подгруппой 3.
    """

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
