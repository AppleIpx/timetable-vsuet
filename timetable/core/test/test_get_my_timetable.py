import datetime
from datetime import timedelta
from unittest.mock import patch

import pytest
from django.utils import timezone
from rest_framework import status

from timetable.core.api.serializers.list_subject_serializer import SubjectMeSerializer
from timetable.core.api.utils import get_two_week_range
from timetable.core.test.factories.subject import SubjectFactory


def create_subjects(student=None, teacher=None):
    today = datetime.date(2025, 7, 16)
    start_weekday, end_weekday = get_two_week_range(today)

    # Предметы: 3 не попадают в диапазон
    _ = [
        SubjectFactory(
            group=student.group,
            subgroup=student.subgroup,
            date=start_weekday - timedelta(days=1),  # например, 13 июля
            teacher=teacher,
        ),
        SubjectFactory(
            group=student.group,
            subgroup=student.subgroup,
            date=end_weekday + timedelta(days=1),  # например, 28 июля
            teacher=teacher,
        ),
        SubjectFactory(
            group=student.group,
            subgroup=student.subgroup,
            date=start_weekday - timedelta(days=10),  # далеко вне диапазона
            teacher=teacher,
        ),
    ]
    # Предметы: 2 попадают в диапазон
    if teacher:
        return [
            SubjectFactory(
                group=student.group,
                subgroup=student.subgroup,
                date=start_weekday + timedelta(days=1),  # например, 15 июля
                teacher=teacher,
            ),
            SubjectFactory(
                group=student.group,
                subgroup=student.subgroup,
                date=end_weekday,  # например, 27 июля
                teacher=teacher,
            ),
        ]
    return [
        SubjectFactory(
            group=student.group,
            subgroup=student.subgroup,
            date=start_weekday + timedelta(days=1),  # например, 15 июля
        ),
        SubjectFactory(
            group=student.group,
            subgroup=student.subgroup,
            date=end_weekday,  # например, 27 июля
        ),
    ]


@pytest.mark.django_db
@patch("timetable.core.api.views.list_timetable.timezone.now")
def test_get_students_timetable(mock_now, create_api_client, student):
    """
    Тест проверяет, что авторизированному пользователю(студенту) возвращается его расписание на 2 недели
    с 14.07.2025 по 27.07.2025 включительно.
    Например, сегодня 16 июля и делая запрос пользователь получит расписание начиная с 14 июля
    и заканчивая 27 июля включительно.
    """
    mock_now.return_value = datetime.datetime(2025, 7, 16, tzinfo=timezone.get_current_timezone())
    subjects_in_range = create_subjects(student=student)

    client = create_api_client(student.user)
    response = client.get("/api/timetable/me/")
    response_data = response.json()

    current_date = timezone.now().date()
    start_weekday, end_weekday = get_two_week_range(current_date)

    serializer = SubjectMeSerializer(
        subjects_in_range,
        many=True,
        context={
            "request": response.wsgi_request,
            "start_weekday": start_weekday,
            "end_weekday": end_weekday,
        },
    )

    expected_data = serializer.data

    assert response.status_code == status.HTTP_200_OK
    assert response_data == expected_data
    assert response.status_code == status.HTTP_200_OK
    assert len(response_data) == len(subjects_in_range)


@pytest.mark.django_db
@patch("timetable.core.api.views.list_timetable.timezone.now")
def test_get_teachers_timetable(mock_now, create_api_client, teacher, student):
    """
    Тест проверяет, что авторизированному пользователю(преподавателю)
    возвращается его расписание на 2 недели с 14.07.2025 по 27.07.2025 включительно.
    Например, сегодня 16 июля и делая запрос пользователь получит расписание начиная с 14 июля
    и заканчивая 27 июля включительно.
    """
    mock_now.return_value = datetime.datetime(2025, 7, 16, tzinfo=timezone.get_current_timezone())
    subjects_in_range = create_subjects(student=student, teacher=teacher)

    client = create_api_client(teacher.user)
    response = client.get("/api/timetable/me/")
    response_data = response.json()

    current_date = timezone.now().date()
    start_weekday, end_weekday = get_two_week_range(current_date)

    serializer = SubjectMeSerializer(
        subjects_in_range,
        many=True,
        context={
            "request": response.wsgi_request,
            "start_weekday": start_weekday,
            "end_weekday": end_weekday,
        },
    )

    expected_data = serializer.data

    assert response.status_code == status.HTTP_200_OK
    assert response_data == expected_data
    assert response.status_code == status.HTTP_200_OK
    assert len(response_data) == len(subjects_in_range)
