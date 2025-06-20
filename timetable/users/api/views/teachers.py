from rest_framework import mixins
from rest_framework import viewsets

from timetable.users.api.serializers import TeacherSerializer
from timetable.users.models import Teacher


class TeacherView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
