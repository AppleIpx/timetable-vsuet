from django.contrib import admin


class DayOfWeekFilter(admin.SimpleListFilter):
    title = "день недели"
    parameter_name = "type_of_day"

    # Желаемый порядок
    ORDERED_DAYS = [
        "понедельник",
        "вторник",
        "среда",
        "четверг",
        "пятница",
        "суббота",
    ]

    def lookups(self, request, model_admin):
        # Возвращаем только те дни, которые реально есть в БД, но в нужном порядке
        qs = model_admin.model.objects.values_list("type_of_day", flat=True).distinct()
        existing_days = sorted(
            set(qs),
            key=lambda day: self.ORDERED_DAYS.index(day.lower()) if day.lower() in self.ORDERED_DAYS else 999,
        )
        return [(day, day.capitalize()) for day in existing_days]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(type_of_day=self.value())
        return queryset
