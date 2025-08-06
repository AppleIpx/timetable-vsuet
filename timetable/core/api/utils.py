from datetime import timedelta

from django.db.models import Exists
from django.db.models import OuterRef
from django.db.models import Q

from timetable.core.models import SubjectRepeat


def get_two_week_range(current_date):
    start_of_week = current_date - timedelta(days=current_date.weekday())
    end_of_next_week = start_of_week + timedelta(days=13)
    return start_of_week, end_of_next_week


def filter_by_date_range(queryset, date_min=None, date_max=None):
    """
    Фильтрует queryset модели Subject по дате занятия (поле `date`) или по датам повторений (`repeat_dates__date`).

    Как работает:
    1. Создаётся Q-объект (`date_filter`), который фильтрует предметы по полю `Subject.date`.
       - Если указан `date_min`, добавляется фильтрация `date >= date_min`.
       - Если указан `date_max`, добавляется фильтрация `date <= date_max`.

    2. Создаётся подзапрос (`repeat_dates_qs`), который ищет записи в `SubjectRepeat`, связанные с конкретным
    `Subject` (через `OuterRef("pk")`).
       - К этому подзапросу применяются те же условия фильтрации по дате: `date >= date_min`, `date <= date_max`.

    3. Основной `queryset` фильтруется:
       - либо по полю `Subject.date` через `date_filter`,
       - либо по существованию хотя бы одной подходящей записи в `SubjectRepeat` через `Exists(repeat_dates_qs)`.

    То есть: вернутся только те `Subject`, у которых:
    - либо `date` попадает в диапазон,
    - либо есть хотя бы одно `repeat_date`, которое попадает в диапазон.

    Аргументы:
        queryset (QuerySet): Исходный queryset модели Subject.
        date_min (date | None): Минимальная дата (включительно).
        date_max (date | None): Максимальная дата (не включительно).

    Возвращает:
        QuerySet: Отфильтрованный список занятий.
    """
    # Q-объект для Subject.date
    date_filter = Q()
    if date_min:
        date_filter &= Q(date__gte=date_min)
    if date_max:
        date_filter &= Q(date__lte=date_max)

    # Подзапрос для repeat_dates
    repeat_dates_qs = SubjectRepeat.objects.filter(subject=OuterRef("pk"))
    if date_min:
        repeat_dates_qs = repeat_dates_qs.filter(date__gte=date_min)
    if date_max:
        repeat_dates_qs = repeat_dates_qs.filter(date__lte=date_max)

    return queryset.filter(
        date_filter | Exists(repeat_dates_qs),
    ).distinct()
