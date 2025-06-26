import pytest
from rest_framework import status


@pytest.mark.django_db
def test_user_info_student(user_api_client, user, student):
    student.user = user
    student.save()

    response = user_api_client.get("/api/users/me/")
    response_data = response.json()["data"]

    assert response.status_code == status.HTTP_200_OK
    assert response.data["role"] == "student"
    assert response_data["id"] == student.id
    assert response_data["first_name"] == student.first_name
    assert response_data["last_name"] == student.last_name
    assert response_data["patronymic"] == student.patronymic
    assert response_data["gradebook"] == student.gradebook
    assert response_data["group"] == {"id": student.group.id, "name": student.group.name}
    assert response_data["faculty"] == {"id": student.faculty.id, "name": student.faculty.name}
    assert response_data["subgroup"] == student.subgroup


@pytest.mark.django_db
def test_user_info_teacher(user_api_client, user, teacher):
    teacher.user = user
    teacher.save()

    response = user_api_client.get("/api/users/me/")
    response_data = response.json()["data"]

    assert response.status_code == status.HTTP_200_OK
    assert response.data["role"] == "teacher"
    assert response_data["id"] == teacher.id
    assert response_data["first_name"] == teacher.first_name
    assert response_data["last_name"] == teacher.last_name
    assert response_data["patronymic"] == teacher.patronymic


@pytest.mark.django_db
def test_user_info_unknown(user_api_client):
    response = user_api_client.get("/api/users/me/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["role"] == "unknown"
    assert response.data["user"] == "Anonymous"


@pytest.mark.django_db
def test_user_info_unauthorized(unauthorized_api_client):
    response = unauthorized_api_client.get("/api/users/me/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Authentication credentials were not provided."
