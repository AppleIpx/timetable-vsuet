from datetime import timedelta
from urllib.parse import urlencode

import pytest
from django.utils import timezone
from rest_framework import status

from timetable.core.enums import DENOMINATOR
from timetable.core.enums import LECTURE
from timetable.core.enums import NUMERATOR
from timetable.core.models import Subject
from timetable.core.test.factories.subject import SubjectFactory

pytestmark = pytest.mark.django_db


def create_dates_for_subjects(anchor):
    """
    Возвращает список из 5 дат в пределах семестра, заданного объектом anchor.

    - 1-я дата: начало семестра
    - 2-я дата: конец семестра
    - 3-я, 4-я, 5-я: даты в середине семестра, равномерно распределённые
    """
    start = anchor.start_date
    end = anchor.end_date
    delta = (end - start).days

    # Даты:
    date_1 = start  # начало
    date_2 = end  # конец
    date_3 = start + timedelta(days=delta // 3)
    date_4 = start + timedelta(days=(delta * 2) // 3)
    date_5 = start + timedelta(days=delta // 2)

    return [date_1, date_2, date_3, date_4, date_5]


def get_expected_result(
    expected_subjects: list[Subject],
    response_data: dict,
):
    returned_ids = {item["id"] for item in response_data}
    expected_ids = {s.id for s in expected_subjects}
    assert len(response_data) == len(expected_subjects)
    return expected_ids, returned_ids


def create_some_subjects(anchor):
    """
    Создаёт 5 объектов Subject с разными датами в пределах семестра.

    Даты выбираются с помощью функции create_dates_for_subjects:
    начало, конец и три даты в середине.
    """
    dates = create_dates_for_subjects(anchor)
    return [SubjectFactory(date=date) for date in dates]


def test_filter_date_max_subject(user_api_client, start_semester):
    """
    Тестирует фильтрацию расписания по максимальной дате (date_max).

    Проверяет, что API возвращает только предметы, у которых дата не превышает указанный date_max.
    """
    subjects = create_some_subjects(start_semester)
    date_max = timezone.localdate() + timedelta(days=60)
    params = {"date_max": date_max.isoformat()}
    url = f"/api/timetable/?{urlencode(params)}"
    response = user_api_client.get(url)

    # Ожидаем: только те предметы, у которых date <= date_max
    response_data = response.json()
    expected_subjects = [s for s in subjects if s.date <= date_max]

    returned_ids, expected_ids = get_expected_result(expected_subjects, response_data)

    assert response.status_code == status.HTTP_200_OK
    assert returned_ids == expected_ids


def test_filter_date_min_subject(user_api_client, start_semester):
    """
    Тестирует фильтрацию расписания по миниммальной дате (date_min).

    Проверяет, что API возвращает только предметы, у которых дата превышает указанный date_min.
    """
    subjects = create_some_subjects(start_semester)
    date_min = timezone.localdate() + timedelta(days=60)
    params = {"date_max": date_min.isoformat()}
    url = f"/api/timetable/?{urlencode(params)}"
    response = user_api_client.get(url)
    response_data = response.json()
    expected_subjects = [s for s in subjects if date_min >= s.date]

    returned_ids, expected_ids = get_expected_result(expected_subjects, response_data)

    assert response.status_code == status.HTTP_200_OK
    assert returned_ids == expected_ids


def test_filter_group_name_subject(user_api_client, start_semester, group):
    """
    Тестирует фильтрацию расписания по названию группы (group__name).

    Проверяет, что API возвращает только те предметы, в которых указана
    введенная группа
    """
    some_subjects = create_some_subjects(start_semester)
    subjects_with_group = SubjectFactory.create_batch(3, group=group)
    subjects = some_subjects + subjects_with_group
    params = {"group__name": group.name}
    url = f"/api/timetable/?{urlencode(params)}"
    response = user_api_client.get(url)
    response_data = response.json()
    expected_subjects = [s for s in subjects if group.name == s.group.name]
    returned_ids, expected_ids = get_expected_result(expected_subjects, response_data)

    assert response.status_code == status.HTTP_200_OK
    assert returned_ids == expected_ids


@pytest.mark.parametrize(
    ("subgroup", "expected_subgroups"),
    [
        (1, {1, 3}),
        (2, {2, 3}),
        (3, {3}),
    ],
)
def test_filter_subgroup_subject(user_api_client, start_semester, subgroup, expected_subgroups):
    """
    Проверяет фильтрацию расписания по подгруппе.

    Ожидается следующая логика:
    - Если указана подгруппа 1, возвращаются предметы с подгруппой 1 и общей (3).
    - Если указана подгруппа 2, возвращаются предметы с подгруппой 2 и общей (3).
    - Если указана подгруппа 3 (общая), возвращаются только предметы с подгруппой 3.

    Тест создает по два предмета на каждую из подгрупп (1, 2, 3) и проверяет,
    что API возвращает корректный список предметов согласно указанной подгруппе.
    """
    subjects_with_subgroup_1 = SubjectFactory.create_batch(2, subgroup=1)
    subjects_with_subgroup_2 = SubjectFactory.create_batch(2, subgroup=2)
    subjects_with_subgroup_3 = SubjectFactory.create_batch(2, subgroup=3, type_of_classes=LECTURE)
    subjects = subjects_with_subgroup_1 + subjects_with_subgroup_2 + subjects_with_subgroup_3

    params = {"subgroup": subgroup}
    url = f"/api/timetable/?{urlencode(params)}"
    response = user_api_client.get(url)
    response_data = response.json()

    expected_subjects = [s for s in subjects if s.subgroup in expected_subgroups]
    returned_ids, expected_ids = get_expected_result(expected_subjects, response_data)

    assert response.status_code == status.HTTP_200_OK
    assert returned_ids == expected_ids


@pytest.mark.parametrize(
    "type_of_week",
    [NUMERATOR, DENOMINATOR],
)
def test_filter_type_of_week_subject(user_api_client, start_semester, type_of_week):
    """
    Проверяет фильтрацию расписания по типу недели (Числитель или Знаменатель).

    Тест создает по два предмета с типами недели "Числитель" и "Знаменатель",
    после чего проверяет, что API возвращает только те занятия,
    у которых тип недели соответствует переданному в параметре `type_of_week`.
    """
    subjects_with_numerator = SubjectFactory.create_batch(2, type_of_week=NUMERATOR)
    subjects_with_denominator = SubjectFactory.create_batch(2, type_of_week=DENOMINATOR)
    subjects = subjects_with_numerator + subjects_with_denominator
    expected_subjects = [s for s in subjects if s.type_of_week == type_of_week]

    params = {"type_of_week": type_of_week}
    url = f"/api/timetable/?{urlencode(params)}"
    response = user_api_client.get(url)
    response_data = response.json()

    returned_ids, expected_ids = get_expected_result(expected_subjects, response_data)

    assert response.status_code == status.HTTP_200_OK
    assert returned_ids == expected_ids
