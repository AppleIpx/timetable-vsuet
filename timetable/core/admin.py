from django.contrib import admin

from timetable.core.models import Audience
from timetable.core.models import Faculty
from timetable.core.models import Group
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


admin.site.register(Faculty)
admin.site.register(Group)
admin.site.register(TimeSubject)
