from rest_framework import serializers

from timetable.core.models import Audience
from timetable.core.serializers.list_subject_serializer import SubjectSerializer


class AudienceWithSubjectsSerializer(serializers.ModelSerializer):
    subjects = serializers.SerializerMethodField()

    class Meta:
        model = Audience
        fields = ("id", "name", "subjects")

    def get_subjects(self, obj):
        subjects = getattr(obj, "subject_set", []).all()
        return SubjectSerializer(subjects, many=True).data
