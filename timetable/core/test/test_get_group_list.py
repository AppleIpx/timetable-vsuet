import pytest
from rest_framework import status

from timetable.core.models import Group
from timetable.core.test.factories.group import GroupFactory


@pytest.mark.django_db
def test_get_group_list(user_api_client):
    GroupFactory.create_batch(5)
    response = user_api_client.get("/api/timetable/group/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "id": group.id,
            "name": group.name,
        }
        for group in Group.objects.all()
    ]
