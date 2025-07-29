import pytest
from rest_framework import status


@pytest.mark.django_db
def test_get_subjects_in_audience(user_api_client, subject_with_everyweek_repeat):
    """Тест проверяет, что по конкретной аудитории можно получить список предметов, которые будут в ней проводиться"""
    audience = subject_with_everyweek_repeat[0].audience
    response = user_api_client.get(f"/api/timetable/audience/{audience.id}/")
    response_data = response.json()

    expected_subjects = [
        {
            "id": subject.id,
            "name": subject.name,
            "date": str(subject.date),
            "audience": {
                "id": subject.audience.id,
                "name": subject.audience.name,
            },
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
            "repeat_dates": [
                {
                    "id": rd.id,
                    "date": str(rd.date),
                }
                for rd in subject.repeat_dates.all()
            ],
        }
        for subject in subject_with_everyweek_repeat
    ]

    assert response.status_code == status.HTTP_200_OK
    assert response_data["id"] == audience.id
    assert response_data["name"] == audience.name
    assert response_data["subjects"] == expected_subjects
