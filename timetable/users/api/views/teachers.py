from rest_framework.viewsets import ReadOnlyModelViewSet

from timetable.users.api.serializers import TeacherDetailSerializer
from timetable.users.api.serializers import TeacherListSerializer
from timetable.users.models import Teacher


class TeacherView(ReadOnlyModelViewSet):
    def get_queryset(self):
        return Teacher.objects.prefetch_related("subjects")

    def get_serializer_class(self):
        if self.action == "list":
            return TeacherListSerializer
        if self.action == "retrieve":
            return TeacherDetailSerializer
        return super().get_serializer_class()
