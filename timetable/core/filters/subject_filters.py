from datetime import UTC

from django.db.models import Q
from django_filters import rest_framework as filters

from timetable.core.enums import FILTER_TYPE_OF_WEEK_CHOICES
from timetable.core.models import Subject


class SubjectFilter(filters.FilterSet):
    date_min = filters.DateTimeFilter(method="filter_by_date_min", label="Дата начала или повторения после")
    date_max = filters.DateTimeFilter(method="filter_by_date_max", label="Дата начала или повторения до")

    type_of_week = filters.ChoiceFilter(choices=FILTER_TYPE_OF_WEEK_CHOICES)
    group__name = filters.CharFilter(field_name="group__name", lookup_expr="exact")
    subgroup = filters.NumberFilter(field_name="subgroup", lookup_expr="exact")

    def filter_by_date_min(self, queryset, name, value):
        """Фильтр по дате начала или повторения после выбранной даты."""
        utc_value = value.replace(tzinfo=UTC)
        return queryset.filter(Q(date__gte=utc_value) | Q(repeat_dates__date__gte=utc_value)).distinct()

    def filter_by_date_max(self, queryset, name, value):
        """Фильтр по дате начала или повторения до выбранной даты."""
        utc_value = value.replace(tzinfo=UTC)
        return queryset.filter(Q(date__lte=utc_value) | Q(repeat_dates__date__lte=utc_value)).distinct()

    class Meta:
        model = Subject
        fields = ["type_of_week", "group__name", "subgroup", "date_min", "date_max"]
