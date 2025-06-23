from rest_framework import serializers


class TeacherSearchSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    patronymic = serializers.CharField()
