from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view
from rest_framework.generics import ListAPIView

from timetable.search.api.serializers.request_serializer import RequestSearchSerializer
from timetable.search.api.serializers.teacher_serializer import TeacherSearchSerializer
from timetable.search.api.utils.django_filter import django_filter_warning
from timetable.search.query_generators.teacher_search_query_generator import TeacherSearchQueryGenerator


@extend_schema_view(get=extend_schema(parameters=[RequestSearchSerializer]))
class TeacherSearchView(ListAPIView):
    """
    # Поиск преподавателей по части имени, фамилии или отчеству.

    ## Данный эндпоинт позволяет выполнять "умный" полнотекстовый поиск преподавателей
    ## с поддержкой:
    - поиска по первой части слова,
    - поиска с учетом опечаток,
    - поиска по подстроке.

    ## Поиск производится по полям:
    - `first_name` — имя,
    - `last_name` — фамилия,
    - `patronymic` — отчество.

    ## Параметры запроса:
    - `query` (str, min_length=2): Поисковая строка, по которой будет производиться поиск.

    ## Возвращает:
    - Список преподавателей.
    """

    request_serializer_class = RequestSearchSerializer
    serializer_class = TeacherSearchSerializer

    @django_filter_warning  # type: ignore[arg-type]
    def get_queryset(self):
        serializer = self.request_serializer_class(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)
        query_generator_service = TeacherSearchQueryGenerator()
        return query_generator_service(**serializer.validated_data).execute()
