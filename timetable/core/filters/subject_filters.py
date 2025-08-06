from django.db.models import Q
from django_filters import rest_framework as filters

from timetable.core.api.utils import filter_by_date_range
from timetable.core.enums import FILTER_TYPE_OF_WEEK_CHOICES
from timetable.core.models import Subject


class SubjectFilter(filters.FilterSet):
    date_max = filters.DateTimeFilter(method="filter_by_date_max", label="Дата начала или повторения до")
    date_min = filters.DateTimeFilter(method="filter_by_date_min", label="Дата начала или повторения после")

    type_of_week = filters.ChoiceFilter(choices=FILTER_TYPE_OF_WEEK_CHOICES)
    group__name = filters.CharFilter(field_name="group__name", lookup_expr="exact")
    subgroup = filters.NumberFilter(method="filter_by_subgroup", label="Подгруппа")

    def filter_by_date_min(self, queryset, name, value):
        """Фильтр по дате начала или повторения после выбранной даты."""
        date_max = self.data.get("date_max")
        return filter_by_date_range(queryset, date_min=value, date_max=date_max)

    def filter_by_date_max(self, queryset, name, value):
        """Фильтр по дате начала или повторения до выбранной даты."""
        date_min = self.data.get("date_min")
        return filter_by_date_range(queryset, date_min=date_min, date_max=value)

    def filter_by_subgroup(self, queryset, name, value):
        """
        Если фильтр по подгруппе передан — ищем только по ней и по лекциям (3).
        Если фильтр не передан — возвращаем всё (в т.ч. лекции).
        """
        if value in (1, 2):
            return queryset.filter(Q(subgroup=value) | Q(subgroup=3))
        if value == 3:  # noqa: PLR2004
            return queryset.filter(subgroup=3)
        return queryset

    class Meta:
        model = Subject
        fields = ["type_of_week", "group__name", "subgroup", "date_min", "date_max"]
