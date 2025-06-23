import pytest
from rest_framework import status

from timetable.search.documents.subject_doc import SubjectDocument
from timetable.search.documents.teacher_doc import TeacherDocument


@pytest.mark.django_db
def test_get_teacher_detail_by_filter(user_api_client, teacher):
    """
    Тест проверяет, что при указании не менее 3 символов в полях,
    будет выводиться нужный список преподавателей совпадающие с введенными символами через OpenSearch.
    """

    TeacherDocument().update([teacher], action="index")
    prefix = teacher.first_name[:3]

    response = user_api_client.get(
        "/api/search/teachers/",
        data={"query": prefix},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "id": teacher.id,
            "first_name": teacher.first_name,
            "last_name": teacher.last_name,
            "patronymic": teacher.patronymic,
        },
    ]


@pytest.mark.django_db
def test_get_subject_detail_by_filter(user_api_client, subject):
    """
    Тест проверяет, что при указании не менее 3 символов в полях,
    будет выводиться нужный список предметов совпадающие с введенными символами через OpenSearch.
    """
    SubjectDocument().update([subject], action="index")
    prefix = subject.name[:3]
    response = user_api_client.get(
        "/api/search/subjects/",
        data={"query": prefix},
    )
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    subject_data = data[0]

    assert subject_data["id"] == subject.id
    assert subject_data["name"] == subject.name

    assert subject_data["audience"]["id"] == subject.audience.id
    assert subject_data["audience"]["name"] == subject.audience.name

    assert subject_data["type_of_day"] == subject.type_of_day
    assert subject_data["type_of_week"] == subject.type_of_week
    assert subject_data["type_of_classes"] == subject.type_of_classes

    assert subject_data["time_subject"]["number"] == subject.time_subject.number
    assert subject_data["time_subject"]["start_time"] == str(subject.time_subject.start_time)
    assert subject_data["time_subject"]["end_time"] == str(subject.time_subject.end_time)

    assert subject_data["teacher"]["id"] == subject.teacher.id
    assert subject_data["teacher"]["first_name"] == subject.teacher.first_name
    assert subject_data["teacher"]["last_name"] == subject.teacher.last_name
    assert subject_data["teacher"]["patronymic"] == subject.teacher.patronymic

    assert subject_data["group"]["id"] == subject.group.id
    assert subject_data["group"]["name"] == subject.group.name

    assert subject_data["subgroup"] == subject.subgroup
