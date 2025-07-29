from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import extend_schema_view
from rest_framework.generics import ListAPIView

from timetable.core.api.serializers.list_subject_serializer import SubjectSerializer
from timetable.core.models import Subject
from timetable.search.api.serializers.request_serializer import RequestSearchSerializer
from timetable.search.api.utils.django_filter import django_filter_warning
from timetable.search.query_generators.subject_search_query_generator import SubjectSearchQueryGenerator


@extend_schema_view(get=extend_schema(parameters=[RequestSearchSerializer]))
class SubjectSearchView(ListAPIView):
    """
    # Поиск занятий по ключевому слову.

    Данный эндпоинт позволяет искать занятия по произвольному текстовому запросу.
    Поддерживается нечеткий поиск и подстановки, что позволяет находить результаты даже при
    наличии опечаток или неполных данных.

    ## Что можно искать:
    - Названия предметов
    - ФИО преподавателя (имя, фамилия, отчество)
    - Название аудитории
    - Название группы

    ## Типы поиска:
    - полнотекстовый поиск с учетом морфологии и опечаток
    - точное совпадение по ключу `group_name`
    - подстановочный поиск (например, `*иван*` найдёт `Иван`, `Иванов`, `Сиванов` и т.д.)

    ## Параметры:
    - `query` (строка, обязательный, минимум 2 символа) — поисковый запрос.

    ## Примеры запросов:
    - `Базы данных` — найдёт все занятия с названием предмета "Базы данных".
    - `Иванов` — найдёт занятия, которые ведёт преподаватель с фамилией Иванов.
    - `У-123` — найдёт занятия для группы У-123.
    - `302` — найдёт занятия в указанной аудитории.

    ## Примечания:
    - Поиск осуществляется по индексу OpenSearch.
    - Возвращаются только те занятия, которые существуют в базе данных.

    ## Требуется только GET-запрос, авторизация не обязательна.
    """

    request_serializer_class = RequestSearchSerializer
    serializer_class = SubjectSerializer

    @django_filter_warning  # type: ignore[arg-type]
    def get_queryset(self):
        serializer = self.request_serializer_class(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)

        query_generator_service = SubjectSearchQueryGenerator()
        search_result = query_generator_service(**serializer.validated_data).execute()

        subject_ids = [hit.meta.id for hit in search_result]
        return (
            Subject.objects.filter(id__in=subject_ids)
            .select_related("teacher", "group", "audience", "time_subject")
            .prefetch_related("repeat_dates")
        )
