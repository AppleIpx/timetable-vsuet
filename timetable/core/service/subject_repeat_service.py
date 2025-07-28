from abc import ABC
from abc import abstractmethod
from datetime import date
from datetime import datetime
from datetime import timedelta

from django.conf import settings
from django.db import transaction
from pytz import timezone

from timetable.core.enums import WITHOUT_REPETITION
from timetable.core.enums import EveryTwoWeeks
from timetable.core.enums import EveryWeek
from timetable.core.models import ScheduleAnchor
from timetable.core.models import Subject
from timetable.core.models import SubjectRepeat

MOSCOW_TZ = timezone("Europe/Moscow")


class BaseRepeatDateUpdater(ABC):
    """Базовый класс для создания дат повторения."""

    def __init__(self, subject: Subject):
        self.subject = subject
        self.start_date = subject.date
        self.end_date = self._get_schedule_end_date()

    def _get_schedule_end_date(self) -> date:
        anchor = ScheduleAnchor.objects.first()
        if not anchor:
            msg_error = "Не найдена опорная дата расписания."
            raise ValueError(msg_error)
        return anchor.end_date

    @abstractmethod
    def get_step(self) -> int:
        """Возвращает шаг повторения в днях."""

    def create_repeat_dates(self) -> list[SubjectRepeat]:
        """
        Генерирует список объектов `SubjectRepeat` с датами повторения занятия.

        Метод используется для создания списка дат, на которые должно приходиться повторение занятия (`Subject`)
        с учётом определённого шага повторения.
        Повторения происходят только в те же дни недели, что и оригинальное занятие.

        Алгоритм:
        - Вычисляется целевой день недели (weekday) исходного занятия.
        - Итеративно добавляются дни с шагом `step` (в днях), начиная от `start_date + step` до `end_date`.
        - Если очередная дата попадает на тот же день недели, что и оригинальное занятие, она добавляется в список.

        Returns:
            list[SubjectRepeat]: Список объектов `SubjectRepeat`,
            каждый из которых представляет одно повторение занятия
            на соответствующую дату.
        """
        repeat_dates = []
        step = self.get_step()
        current_date = self.start_date + timedelta(days=step)
        target_weekday = self.subject.date.weekday()
        base_time = self.subject.time_subject.start_time

        while current_date <= self.end_date:
            if current_date.weekday() == target_weekday:
                naive_dt = datetime.combine(current_date, base_time)
                aware_dt = MOSCOW_TZ.localize(naive_dt)
                repeat_dates.append(SubjectRepeat(subject=self.subject, date=aware_dt))
            current_date += timedelta(days=step)
        return repeat_dates


class WeeklyRepeatDateUpdater(BaseRepeatDateUpdater):
    """Создает даты для еженедельного повторения."""

    def get_step(self) -> int:
        return 7


class TwoWeeklyRepeatDateUpdater(BaseRepeatDateUpdater):
    """Создает даты для двухнедельного повторения."""

    def get_step(self) -> int:
        return 14


class SubjectRepeatService:
    _updaters: dict[str, type[BaseRepeatDateUpdater]] = {
        EveryWeek: WeeklyRepeatDateUpdater,
        EveryTwoWeeks: TwoWeeklyRepeatDateUpdater,
    }

    def __init__(self, subject: Subject):
        self.subject = subject

    def __call__(self) -> None:
        """Входная точка сервиса."""
        self._create_event_repeat_dates()

    @transaction.atomic
    def _create_event_repeat_dates(self) -> None:
        updater_class = self._updaters.get(self.subject.rule_of_repeat)
        if not updater_class:
            msg_error = "Неизвестный тип повторения."
            raise ValueError(msg_error)
        if self.subject.rule_of_repeat == WITHOUT_REPETITION:
            return

        self.subject.repeat_dates.all().delete()
        updater = updater_class(self.subject)
        repeat_dates = updater.create_repeat_dates()
        SubjectRepeat.objects.bulk_create(repeat_dates)

        if settings.USE_OPENSEARCH:
            self.update_opensearch_subjects_index(repeat_dates=repeat_dates)

    def update_opensearch_subjects_index(self, repeat_dates: list[SubjectRepeat]) -> None:
        # SubjectDocument.search().filter("term", id=self.subject.id).delete()  # noqa: ERA001
        # SubjectDocument().update([self.subject], action="index")  # noqa: ERA001
        ...
