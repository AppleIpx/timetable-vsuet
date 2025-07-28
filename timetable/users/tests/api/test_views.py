import pytest
from starlette import status

from timetable.core.enums import EveryWeek
from timetable.users.models import Teacher
from timetable.users.tests.factories import TeacherFactory


@pytest.mark.django_db
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


@pytest.mark.django_db
def test_get_teacher_detail(user_api_client, teacher, subject):
    subject.teacher = teacher
    subject.rule_of_repeat = EveryWeek
    subject.save()

    response = user_api_client.get(f"/api/users/teachers/{teacher.id}/")
    response_data = response.json()

    expected_subjects = [
        {
            "id": sub.id,
            "name": sub.name,
            "date": str(subject.date),
            "audience": {
                "id": sub.audience.id,
                "name": sub.audience.name,
            },
            "type_of_week": sub.type_of_week,
            "type_of_classes": sub.type_of_classes,
            "time_subject": {
                "number": sub.time_subject.number,
                "start_time": str(sub.time_subject.start_time),
                "end_time": str(sub.time_subject.end_time),
            },
            "teacher": {
                "id": teacher.id,
                "first_name": teacher.first_name,
                "last_name": teacher.last_name,
                "patronymic": teacher.patronymic,
            },
            "group": {
                "id": sub.group.id,
                "name": sub.group.name,
            },
            "subgroup": sub.subgroup,
            "repeat_dates": [
                {
                    "id": rd.id,
                    "date": str(rd.date),
                }
                for rd in subject.repeat_dates.all()
            ],
        }
        for sub in teacher.subjects.all()
    ]

    assert response.status_code == status.HTTP_200_OK
    assert response_data["id"] == teacher.id
    assert response_data["first_name"] == teacher.first_name
    assert response_data["last_name"] == teacher.last_name
    assert response_data["patronymic"] == teacher.patronymic
    assert response_data["subjects"] == expected_subjects
