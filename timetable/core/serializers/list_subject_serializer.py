from rest_framework import serializers

from timetable.core.models import Subject
from timetable.core.serializers.audience_serializer import AudienceSerializer
from timetable.core.serializers.group_serializer import GroupSerializer
from timetable.core.serializers.time_subject_serializer import TimeSubjectSerializer
from timetable.users.api.serializers import TeacherSerializer


class SubjectSerializer(serializers.ModelSerializer):
    audience = AudienceSerializer()
    time_subject = TimeSubjectSerializer()
    teacher = TeacherSerializer()
    group = GroupSerializer()

    class Meta:
        model = Subject
        fields = (
            "id",
            "name",
            "audience",
            "type_of_day",
            "type_of_week",
            "type_of_classes",
            "time_subject",
            "teacher",
            "group",
            "subgroup",
        )
