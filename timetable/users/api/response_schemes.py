from rest_framework import serializers

from timetable.users.api.serializers import BaseTeacherSerializer
from timetable.users.api.serializers import StudentSerializer


class StudentResponseSerializer(serializers.Serializer):
    role = serializers.CharField()
    data = StudentSerializer()


class TeacherResponseSerializer(serializers.Serializer):
    role = serializers.CharField()
    data = BaseTeacherSerializer()


class UnknownResponseSerializer(serializers.Serializer):
    role = serializers.CharField()
    user = serializers.CharField()
