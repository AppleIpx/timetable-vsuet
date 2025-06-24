import pytest
from rest_framework import status

from timetable.core.test.factories.subject import SubjectFactory


@pytest.mark.django_db
def test_get_subjects_in_audience(user_api_client, audience):
    subjects = SubjectFactory.create_batch(3, audience=audience)

    response = user_api_client.get(f"/api/timetable/audience/{audience.id}/")
    response_data = response.json()

    expected_subjects = [
        {
            "id": subject.id,
            "name": subject.name,
            "audience": {
                "id": audience.id,
                "name": audience.name,
            },
            "type_of_day": subject.type_of_day,
            "type_of_week": subject.type_of_week,
            "type_of_classes": subject.type_of_classes,
            "time_subject": {
                "number": subject.time_subject.number,
                "start_time": str(subject.time_subject.start_time),
                "end_time": str(subject.time_subject.end_time),
            },
            "teacher": {
                "id": subject.teacher.id,
                "first_name": subject.teacher.first_name,
                "last_name": subject.teacher.last_name,
                "patronymic": subject.teacher.patronymic,
            },
            "group": {
                "id": subject.group.id,
                "name": subject.group.name,
            },
            "subgroup": subject.subgroup,
        }
        for subject in subjects
    ]

    assert response.status_code == status.HTTP_200_OK
    assert response_data["id"] == audience.id
    assert response_data["name"] == audience.name
    assert response_data["subjects"] == expected_subjects
