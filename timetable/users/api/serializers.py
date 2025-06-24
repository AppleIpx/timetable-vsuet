from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from timetable.core.serializers.list_subject_serializer import SubjectSerializer
from timetable.users.models import Teacher
from timetable.users.models import User


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["username", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"},
        }


class TeacherListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ("id", "first_name", "last_name", "patronymic")


class TeacherDetailSerializer(TeacherListSerializer):
    subjects = serializers.SerializerMethodField()

    class Meta(TeacherListSerializer.Meta):
        fields = (*TeacherListSerializer.Meta.fields, "subjects")

    @extend_schema_field(SubjectSerializer(many=True))
    def get_subjects(self, obj):
        return SubjectSerializer(obj.subjects.all(), many=True).data
