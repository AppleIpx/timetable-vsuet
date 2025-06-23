from rest_framework import serializers


class RequestSearchSerializer(serializers.Serializer):
    query = serializers.CharField(min_length=3)
