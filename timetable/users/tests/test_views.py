
import pytest
from django.http import HttpRequest
from django.test import RequestFactory
from starlette import status

from timetable.users.api.views.user import UserUpdateView
from timetable.users.models import Teacher
from timetable.users.models import User
from timetable.users.tests.factories import TeacherFactory

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


def test_get_teacher_list(user_api_client):
    """Тест проверяет получение списка преподавателей"""
    response = user_api_client.get("/api/users/teachers/")
    teacher1 = TeacherFactory(first_name="Иван", last_name="Петров", patronymic="Сергеевич")
    teacher2 = TeacherFactory(first_name="Алексей", last_name="Иванов", patronymic="")
    teacher3 = TeacherFactory(first_name="Сергей", last_name="Сидоров", patronymic="Петрович")
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
