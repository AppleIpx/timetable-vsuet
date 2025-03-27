from django.contrib import admin

from timetable.core.models import Faculty
from timetable.core.models import Group
from timetable.core.models import Subject
from timetable.core.models import TimeSubject

admin.site.register(Faculty)
admin.site.register(Group)
admin.site.register(TimeSubject)
admin.site.register(Subject)
