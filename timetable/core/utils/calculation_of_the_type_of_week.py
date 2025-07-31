from datetime import date
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.utils import timezone

from timetable.core.enums import DENOMINATOR
from timetable.core.enums import NUMERATOR


def default_end_date():
    return (timezone.now() + timedelta(days=182)).date()


def calculating_a_type_of_week(target_date: date, start_date_semester) -> str:
    """
    Определяет тип недели (числитель или знаменатель) для указанной даты.

    Алгоритм:
    - Берётся неделя, на которую приходится дата начала семестра (`start_date`).
    - Эта неделя считается "базовой" и соответствует типу недели, указанному в `week_type`
      модели ScheduleAnchor (например, числитель).
    - Далее определяется неделя года для целевой даты (`target_date`).
    - Если номер недели `target_date` совпадает по чётности с номером недели начала семестра,
      то возвращается тот же тип недели.
    - Если чётность разная — возвращается противоположный тип недели.
    """
    if not (start_date_semester and start_date_semester.start_date and start_date_semester.end_date):
        msg_error = "У вас не выставлены даты начала и конца семестра"
        raise ValidationError(msg_error)

    if not (start_date_semester.start_date <= target_date <= start_date_semester.end_date):
        msg_error = (
            f"Дата {target_date} вне диапазона семестра "
            f"({start_date_semester.start_date} – {start_date_semester.end_date})"
        )
        raise ValidationError(msg_error)

    base_week = start_date_semester.start_date.isocalendar()[1]
    target_week = target_date.isocalendar()[1]

    is_same_parity = (base_week % 2) == (target_week % 2)

    if is_same_parity:
        return start_date_semester.week_type
    return DENOMINATOR if start_date_semester.week_type == NUMERATOR else NUMERATOR
