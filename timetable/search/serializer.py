from rest_framework import serializers


class RequestSearchSerializer(serializers.Serializer):
    query = serializers.CharField(min_length=3)


class TeacherSearchSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    patronymic = serializers.CharField()
