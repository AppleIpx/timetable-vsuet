import pytest
from rest_framework import status

from timetable.search.tests.utils import update_teacher_opensearch_index


@pytest.mark.django_db
def test_get_teacher_detail_by_filter(user_api_client, clear_opensearch_indexes, teacher):
    """
    Тест проверяет, что при указании не менее 3 символов в полях,
    будет выводиться нужный список преподавателей совпадающие с введенными символами через OpenSearch.
    """
    update_teacher_opensearch_index(teacher)
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
