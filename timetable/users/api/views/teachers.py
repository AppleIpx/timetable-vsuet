from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import filters
from rest_framework import mixins
from rest_framework import viewsets

from timetable.users.api.serializers import TeacherSerializer
from timetable.users.models import Teacher


class TeacherView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["last_name"]
    search_fields = ["last_name"]
