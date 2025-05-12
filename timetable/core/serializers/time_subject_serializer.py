from rest_framework import serializers

from timetable.core.models import TimeSubject


class TimeSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSubject
        fields = ("number", "start_time", "end_time")
