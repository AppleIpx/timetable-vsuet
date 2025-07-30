import pytest
from rest_framework import status

from timetable.core.test.factories.subject import SubjectFactory
from timetable.search.tests.utils import update_subject_opensearch_index

pytestmark = pytest.mark.django_db


def compare_response(subject, response):
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    subject_data = data[0]

    assert subject_data["id"] == subject.id
    assert subject_data["name"] == subject.name

    assert subject_data["audience"]["id"] == subject.audience.id
    assert subject_data["audience"]["name"] == subject.audience.name

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


def test_get_subject_detail_by_filter(user_api_client, clear_opensearch_indexes, subject):
    """
    Тест проверяет, что при указании не менее 2 символов в полях,
    будет выводиться нужный список предметов совпадающие с введенными символами через OpenSearch.
    """
    subjects = SubjectFactory.create_batch(size=5)
    subjects.append(subject)
    update_subject_opensearch_index(subject)
    prefix = subject.name[:2]
    response = user_api_client.get(
        "/api/search/subjects/",
        data={"query": prefix},
    )
    compare_response(subject, response)


def test_get_subject_detail_by_audience_name_filter(user_api_client, clear_opensearch_indexes, subject):
    """
    Тест проверяет, что если в поиске указать название аудитории(полностью),
    то выведется список всех предметов, которые проводятся в ней
    """
    subjects = SubjectFactory.create_batch(size=5)
    subjects.append(subject)
    update_subject_opensearch_index(subject)
    audience_name = subject.audience.name
    response = user_api_client.get(
        "/api/search/subjects/",
        data={"query": audience_name},
    )
    compare_response(subject, response)


@pytest.mark.parametrize(
    "teacher_field",
    ["first_name", "last_name", "patronymic"],
)
def test_get_subject_detail_by_teacher_field_filter(
    user_api_client,
    clear_opensearch_indexes,
    subject,
    teacher_field,
):
    """
    Тест проверяет, что при фильтрации по имени/фамилии/отчества(по первым 3 символам),
    фамилии или отчеству преподавателя в поиске выводится список всех предметов,
    которые ведет указанный преподаватель.
    """
    update_subject_opensearch_index(subject)

    value = getattr(subject.teacher, teacher_field)
    prefix = value[:3]

    response = user_api_client.get(
        "/api/search/subjects/",
        data={"query": prefix},
    )

    compare_response(subject, response)


def test_get_subject_detail_by_group_name_filter(user_api_client, clear_opensearch_indexes, subject):
    """
    Тест проверяет, что если в поиске указать название учебной группы(полностью),
    то выведется список всех предметов, которые принадлежат этой группе
    """
    subjects = SubjectFactory.create_batch(size=5)
    subjects.append(subject)
    update_subject_opensearch_index(subject)
    group_name = subject.group.name
    response = user_api_client.get(
        "/api/search/subjects/",
        data={"query": group_name},
    )
    compare_response(subject, response)
