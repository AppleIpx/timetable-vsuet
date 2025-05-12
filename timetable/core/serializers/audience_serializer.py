from rest_framework import serializers

from timetable.core.models import Audience


class AudienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audience
        fields = ("name",)
