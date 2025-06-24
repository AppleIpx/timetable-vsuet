from http import HTTPStatus

import pytest
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from django.http import HttpResponseRedirect
from django.test import RequestFactory
from django.urls import reverse
from rest_framework.test import APIRequestFactory
from starlette import status

from timetable.users.api.views.user import UserUpdateView
from timetable.users.api.views.user import UserViewSet
from timetable.users.api.views.user import user_detail_view
from timetable.users.models import Teacher
from timetable.users.models import User
from timetable.users.tests.factories import TeacherFactory
from timetable.users.tests.factories import UserFactory


class TestUserDetailView:
    def test_authenticated(self, user: User, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = UserFactory()
        response = user_detail_view(request, username=user.username)

        assert response.status_code == HTTPStatus.OK

    def test_not_authenticated(self, user: User, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = AnonymousUser()
        response = user_detail_view(request, username=user.username)
        login_url = reverse(settings.LOGIN_URL)

        assert isinstance(response, HttpResponseRedirect)
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == f"{login_url}?next=/fake-url/"


def test_get_teacher_list(user_api_client):
    """Тест проверяет получение списка преподавателей"""
    teacher1 = TeacherFactory(first_name="Иван", last_name="Петров", patronymic="Сергеевич")
    teacher2 = TeacherFactory(first_name="Алексей", last_name="Иванов", patronymic="")
    teacher3 = TeacherFactory(first_name="Сергей", last_name="Сидоров", patronymic="Петрович")
    response = user_api_client.get("/api/users/teachers/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == Teacher.objects.count()

    teacher_ids = {teacher1.id, teacher2.id, teacher3.id}
    response_ids = {teacher["id"] for teacher in response.data}
    assert teacher_ids == response_ids

    teachers_data = {
        teacher1.id: teacher1,
        teacher2.id: teacher2,
        teacher3.id: teacher3,
    }

    for teacher_data in response.data:
        teacher_id = teacher_data["id"]
        teacher_obj = teachers_data[teacher_id]

        assert teacher_data["first_name"] == teacher_obj.first_name
        assert teacher_data["last_name"] == teacher_obj.last_name
        assert teacher_data["patronymic"] == teacher_obj.patronymic


def test_get_teacher_detail(user_api_client, teacher, subject):
    subject.teacher = teacher
    subject.save()
    response = user_api_client.get(f"/api/users/teachers/{teacher.id}/")
    response_data = response.json()

    assert status.HTTP_200_OK == status.HTTP_200_OK
    assert response_data["id"] == teacher.id
    assert response_data["first_name"] == teacher.first_name
    assert response_data["last_name"] == teacher.last_name
    assert response_data["patronymic"] == teacher.patronymic
    assert response_data["subjects"][0]["id"] == subject.id
    assert response_data["subjects"][0]["name"] == subject.name
    assert response_data["subjects"][0]["audience"] == {"id": subject.audience.id, "name": subject.audience.name}
    assert response_data["subjects"][0]["type_of_day"] == subject.type_of_day
    assert response_data["subjects"][0]["type_of_week"] == subject.type_of_week
    assert response_data["subjects"][0]["type_of_classes"] == subject.type_of_classes
    assert response_data["subjects"][0]["time_subject"] == {
        "number": subject.time_subject.number,
        "start_time": str(subject.time_subject.start_time),
        "end_time": str(subject.time_subject.end_time),
    }
    assert response_data["subjects"][0]["teacher"] == {
        "id": teacher.id,
        "first_name": teacher.first_name,
        "last_name": teacher.last_name,
        "patronymic": teacher.patronymic,
    }
    assert response_data["subjects"][0]["group"] == {"id": subject.group.id, "name": subject.group.name}
    assert response_data["subjects"][0]["subgroup"] == subject.subgroup
