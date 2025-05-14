from http import HTTPStatus

import pytest
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from django.http import HttpResponseRedirect
from django.test import RequestFactory
from django.urls import reverse
from rest_framework.test import APITestCase
from starlette import status

from timetable.users.api.views.user import UserUpdateView
from timetable.users.api.views.user import user_detail_view
from timetable.users.models import Teacher
from timetable.users.models import User
from timetable.users.tests.factories import TeacherFactory
from timetable.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestUserUpdateView:
    """
    TODO:
        extracting view initialization code as class-scoped fixture
        would be great if only pytest-django supported non-function-scoped
        fixture db access -- this is a work-in-progress for now:
        https://github.com/pytest-dev/pytest-django/pull/258
    """

    def dummy_get_response(self, request: HttpRequest):
        return None

    def test_get_object(self, user: User, rf: RequestFactory):
        view = UserUpdateView()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_object() == user


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


@pytest.mark.django_db
class TestTeacherListView(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.teacher1 = TeacherFactory(first_name="Иван", last_name="Петров", patronymic="Сергеевич")
        cls.teacher2 = TeacherFactory(first_name="Алексей", last_name="Иванов", patronymic="")
        cls.teacher3 = TeacherFactory(first_name="Сергей", last_name="Сидоров", patronymic="Петрович")

        cls.url = reverse("api:teachers-list")

    def test_get_teacher_list(self):
        """Тест проверяет получение списка преподавателей"""
        response = self.client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == Teacher.objects.count()

        teacher_ids = {self.teacher1.id, self.teacher2.id, self.teacher3.id}
        response_ids = {teacher["id"] for teacher in response.data}
        assert teacher_ids == response_ids

        teachers_data = {
            self.teacher1.id: self.teacher1,
            self.teacher2.id: self.teacher2,
            self.teacher3.id: self.teacher3,
        }

        for teacher_data in response.data:
            teacher_id = teacher_data["id"]
            teacher_obj = teachers_data[teacher_id]

            assert teacher_data["first_name"] == teacher_obj.first_name
            assert teacher_data["last_name"] == teacher_obj.last_name
            assert teacher_data["patronymic"] == teacher_obj.patronymic

    def test_filter_by_last_name(self):
        """Тестируем фильтрацию по фамилии"""
        response = self.client.get(self.url, {"last_name": "Иванов"})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        teacher = Teacher.objects.get(id=response.data[0]["id"])
        assert response.data[0]["id"] == teacher.id
        assert response.data[0]["last_name"] == teacher.last_name
        assert response.data[0]["first_name"] == teacher.first_name
        assert response.data[0]["patronymic"] == teacher.patronymic

    def test_search_by_last_name(self):
        """Тестируем поиск по фамилии"""
        response = self.client.get(self.url, {"search": "Сидо"})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        teacher = Teacher.objects.get(id=response.data[0]["id"])
        assert response.data[0]["id"] == teacher.id
        assert response.data[0]["last_name"] == teacher.last_name
        assert response.data[0]["first_name"] == teacher.first_name
        assert response.data[0]["patronymic"] == teacher.patronymic

    def test_empty_filter_results(self):
        """Тестируем случай, когда фильтр не находит совпадений"""
        response = self.client.get(self.url, {"last_name": "НесуществующаяФамилия"})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0
        assert response.data == []
