from django.contrib import admin

from timetable.core.enums import FILTER_TYPE_OF_WEEK_CHOICES


class TypeOfWeekCustomFilter(admin.SimpleListFilter):
    title = "Тип недели"
    parameter_name = "type_of_week_custom"

    def lookups(self, request, model_admin):
        return FILTER_TYPE_OF_WEEK_CHOICES

    def queryset(self, request, queryset):
        value = self.value()
        if value in dict(FILTER_TYPE_OF_WEEK_CHOICES):
            return queryset.filter(type_of_week=value)
        return queryset
