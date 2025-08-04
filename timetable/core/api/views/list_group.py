from rest_framework import mixins
from rest_framework import viewsets

from timetable.core.api.serializers.group_serializer import GroupSerializer
from timetable.core.models import Group


class GroupViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    # API для получения списка групп.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
