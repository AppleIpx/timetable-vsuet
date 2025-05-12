from rest_framework import serializers

from timetable.users.models import Teacher


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ("full_name",)
