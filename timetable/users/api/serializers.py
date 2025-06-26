from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from timetable.core.api.serializers.faculty_serializer import FacultySerializer
from timetable.core.api.serializers.group_serializer import GroupSerializer
from timetable.core.api.serializers.list_subject_serializer import SubjectSerializer
from timetable.users.models import Student
from timetable.users.models import Teacher


class BaseTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ("id", "first_name", "last_name", "patronymic")


class TeacherListSerializer(BaseTeacherSerializer):
    class Meta(BaseTeacherSerializer.Meta):
        fields = (*BaseTeacherSerializer.Meta.fields,)


class TeacherDetailSerializer(TeacherListSerializer):
    subjects = serializers.SerializerMethodField()

    class Meta(TeacherListSerializer.Meta):
        fields = (*TeacherListSerializer.Meta.fields, "subjects")

    @extend_schema_field(SubjectSerializer(many=True))
    def get_subjects(self, obj):
        return SubjectSerializer(obj.subjects.all(), many=True).data


class StudentSerializer(serializers.ModelSerializer):
    group = GroupSerializer()
    faculty = FacultySerializer()

    class Meta:
        model = Student
        fields = (*TeacherListSerializer.Meta.fields, "gradebook", "group", "faculty", "subgroup")
