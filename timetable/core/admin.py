from django.contrib import admin

from timetable.core.models import Audience
from timetable.core.models import Faculty
from timetable.core.models import Group
from timetable.core.models import ScheduleAnchor
from timetable.core.models import Subject
from timetable.core.models import TimeSubject


@admin.register(Audience)
class AudienceAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_filter = ["type_of_day", "type_of_week"]
    ordering = ["name"]


@admin.register(ScheduleAnchor)
class ScheduleAnchorAdmin(admin.ModelAdmin):
    list_display = ("start_date", "week_type")

    def has_add_permission(self, request):
        return not ScheduleAnchor.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Faculty)
admin.site.register(Group)
admin.site.register(TimeSubject)
