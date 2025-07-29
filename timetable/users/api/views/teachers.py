from drf_spectacular.utils import extend_schema
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

    @extend_schema(
        summary="Список преподавателей",
        description=("Возвращает список всех преподавателей с краткой информацией."),
        responses={200: TeacherListSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Информация о преподавателе",
        description=("Возвращает подробную информацию о преподавателе, включая список предметов, которые он ведёт."),
        responses={200: TeacherDetailSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
