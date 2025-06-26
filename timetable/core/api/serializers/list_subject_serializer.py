from rest_framework import serializers

from timetable.core.api.serializers.group_serializer import GroupSerializer
from timetable.core.api.serializers.time_subject_serializer import TimeSubjectSerializer
from timetable.core.models import Audience
from timetable.core.models import Subject
from timetable.users.models import Teacher


class TeacherSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ("id", "first_name", "last_name", "patronymic")


class AudienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audience
        fields = ("id", "name")


class SubjectSerializer(serializers.ModelSerializer):
    audience = AudienceSerializer()
    time_subject = TimeSubjectSerializer()
    teacher = TeacherSubjectSerializer()
    group = GroupSerializer()

    class Meta:
        model = Subject
        fields = (
            "id",
            "name",
            "audience",
            "date",
            "type_of_day",
            "type_of_week",
            "type_of_classes",
            "time_subject",
            "teacher",
            "group",
            "subgroup",
        )
