import datetime

import pytest
from django.core.exceptions import ValidationError

from timetable.core.enums import AUTO
from timetable.core.enums import NUMERATOR
from timetable.core.test.factories.schedule_anchor import ScheduleAnchorFactory
from timetable.core.test.factories.subject import SubjectFactory

pytestmark = pytest.mark.django_db


def test_subject_without_start_date_semester():
    """Тест проверяет, что нельзя создать предмет не имея дат начала и конца семестра"""
    subject = SubjectFactory(
        date=datetime.date(2025, 9, 8),
        type_of_week=AUTO,
    )

    with pytest.raises(ValidationError) as exc_info:
        subject.clean()

    assert "['У вас не выставлены даты начала и конца семестра']" in str(exc_info.value)


def test_subject_autofill_type_of_week(start_semester):
    """
    Тест проверяет, что если при создании предмета выбрать автоматический
    тип определения типа недели, то он подставит ожидаемый результат.
    Ожидаем тот тип, что указан в start_semester."""
    subject = SubjectFactory(
        type_of_week=AUTO,
        date=start_semester.start_date,
    )
    subject.clean()
    type_of_week = start_semester.week_type
    assert subject.type_of_week == type_of_week


def test_subject_date_outside_semester_range():
    """
    Тест проверяет, что если указать дату проведения занятия вне диапазона периода семестра,
    ожидается ошибка.
    """
    start_date_semester = ScheduleAnchorFactory(
        start_date=datetime.date(2025, 9, 1),
        end_date=datetime.date(2025, 12, 31),
        week_type=NUMERATOR,
    )

    subject = SubjectFactory(
        date=datetime.date(2026, 1, 1),  # После окончания семестра
        type_of_week=AUTO,
    )
    msg_error = (
        f"Дата {subject.date} вне диапазона семестра "
        f"({start_date_semester.start_date} – {start_date_semester.end_date})"
    )

    with pytest.raises(ValidationError) as exc_info:
        subject.clean()

    assert msg_error in str(exc_info.value)
