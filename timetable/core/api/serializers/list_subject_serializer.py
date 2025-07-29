from rest_framework import serializers

from timetable.core.api.serializers.group_serializer import GroupSerializer
from timetable.core.api.serializers.time_subject_serializer import TimeSubjectSerializer
from timetable.core.models import Audience
from timetable.core.models import Subject
from timetable.core.models import SubjectRepeat
from timetable.users.models import Teacher


class TeacherSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ("id", "first_name", "last_name", "patronymic")


class AudienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audience
        fields = ("id", "name")


class SubjectRepeatDateSerializer(serializers.ModelSerializer):
    """Сериализатор для повторяющихся дат мероприятия."""

    class Meta:
        model = SubjectRepeat
        fields = ("id", "date")
        utc_datetime_fields = ("date",)


class SubjectSerializer(serializers.ModelSerializer):
    """Сериализатор для предметов"""

    audience = AudienceSerializer()
    time_subject = TimeSubjectSerializer()
    teacher = TeacherSubjectSerializer()
    group = GroupSerializer()
    repeat_dates = SubjectRepeatDateSerializer(many=True)

    class Meta:
        model = Subject
        fields = (
            "id",
            "name",
            "audience",
            "date",
            "type_of_week",
            "type_of_classes",
            "time_subject",
            "teacher",
            "group",
            "subgroup",
            "repeat_dates",
        )


class SubjectMeSerializer(SubjectSerializer):
    """
    Сериализатор для получения предметов конкретного студента на 2 недели.
    Например, сегодня 17 июля 2025 и сделав запрос предметы выведутся за период с 14.07-27.07
    """

    repeat_dates = serializers.SerializerMethodField()

    class Meta(SubjectSerializer.Meta):
        fields = SubjectSerializer.Meta.fields

    def get_repeat_dates(self, obj):
        return SubjectRepeatDateSerializer(obj.repeat_dates.all(), many=True).data
