from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from timetable.core.api.serializers.list_subject_serializer import SubjectSerializer
from timetable.core.models import Audience


class AudienceWithSubjectsSerializer(serializers.ModelSerializer):
    subjects = serializers.SerializerMethodField()

    class Meta:
        model = Audience
        fields = ("id", "name", "subjects")

    @extend_schema_field(SubjectSerializer(many=True))
    def get_subjects(self, obj):
        subjects = getattr(obj, "subject_set", []).all()
        return SubjectSerializer(subjects, many=True).data
