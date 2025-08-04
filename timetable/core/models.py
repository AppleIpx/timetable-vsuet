import datetime
import logging

from django.core.exceptions import ValidationError
from django.db import models

from timetable.core.enums import AUTO
from timetable.core.enums import FILTER_TYPE_OF_WEEK_CHOICES
from timetable.core.enums import FRIDAY
from timetable.core.enums import LECTURE
from timetable.core.enums import MONDAY
from timetable.core.enums import NUMERATOR
from timetable.core.enums import RULE_OF_REPEATS
from timetable.core.enums import SATURDAY
from timetable.core.enums import SUNDAY
from timetable.core.enums import THURSDAY
from timetable.core.enums import TUESDAY
from timetable.core.enums import TYPE_OF_CLASSES_CHOICES
from timetable.core.enums import TYPE_OF_WEEK_CHOICES
from timetable.core.enums import WEDNESDAY
from timetable.core.enums import WITHOUT_REPETITION
from timetable.core.utils.calculation_of_the_type_of_week import calculating_a_type_of_week
from timetable.core.utils.calculation_of_the_type_of_week import default_end_date
from timetable.users.models import Teacher

logger = logging.getLogger(__name__)


class BaseModel(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")

    class Meta:
        abstract = True


class Faculty(BaseModel):
    class Meta:
        verbose_name = "факультет"
        verbose_name_plural = "факультеты"

    def __str__(self):
        return f"факультет {self.name}"


class Group(BaseModel):
    class Meta:
        verbose_name = "группа"
        verbose_name_plural = "группы"

    def __str__(self):
        return self.name


class Audience(BaseModel):
    class Meta:
        verbose_name = "аудитория"
        verbose_name_plural = "аудитории"

    def __str__(self):
        return f"{self.name}"


class TimeSubject(models.Model):
    number = models.PositiveSmallIntegerField(
        unique=True,
        verbose_name="номер пары по счету",
    )
    start_time = models.TimeField(verbose_name="Время начала пары")
    end_time = models.TimeField(verbose_name="Время окончания пары")

    class Meta:
        verbose_name = "время пары"
        verbose_name_plural = "время пар"

    def __str__(self):
        return f"пара {self.number} с {self.start_time} - {self.end_time}"


class Subject(BaseModel):
    audience = models.ForeignKey(
        Audience,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Аудитория",
    )
    date = models.DateField(
        verbose_name="Дата проведения первого занятия",
        default=datetime.date.today,
    )
    type_of_week = models.CharField(
        max_length=20,
        verbose_name="Тип недели",
        choices=TYPE_OF_WEEK_CHOICES,
        default=AUTO,
    )
    type_of_classes = models.CharField(
        max_length=30,
        verbose_name="Тип занятия",
        choices=TYPE_OF_CLASSES_CHOICES,
        default="",
    )
    rule_of_repeat = models.CharField(
        max_length=30,
        verbose_name="Правило повторения",
        choices=RULE_OF_REPEATS,
        default=WITHOUT_REPETITION,
    )
    time_subject = models.ForeignKey(
        TimeSubject,
        on_delete=models.CASCADE,
        verbose_name="Время пары",
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subjects",
        verbose_name="Преподаватель",
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        verbose_name="Группа",
    )
    subgroup = models.PositiveSmallIntegerField(
        verbose_name="Подгруппа",
        help_text=(
            "Укажите номер подгруппы: 1 или 2 для практик и лабораторных. "
            "Для лекций укажите 3 (означает: для всей группы)."
        ),
    )

    class Meta:
        verbose_name = "предмет"
        verbose_name_plural = "предметы"

    def __str__(self):
        return self.name

    def clean(self):
        start_date_semester = ScheduleAnchor.objects.first()
        type_of_week = calculating_a_type_of_week(
            target_date=self.date,
            start_date_semester=start_date_semester,
        )
        if self.type_of_week == AUTO:
            self.type_of_week = type_of_week

        if self.type_of_week != type_of_week:
            msg_error = f"Тип недели для {self.date} должен быть '{type_of_week}', а не '{self.type_of_week}'."
            raise ValidationError(msg_error)

        if self.type_of_classes == LECTURE and self.subgroup != 3:  # noqa: PLR2004
            msg_error = "Для лекций необходимо указать '3' в поле «Подгруппа» (означает: вся группа)."
            raise ValidationError(msg_error)

        if self.type_of_classes != LECTURE and self.subgroup not in (1, 2):
            msg_error = "Для практических и лабораторных занятий нужно указать подгруппу 1 или 2."
            raise ValidationError(msg_error)


class SubjectRepeat(models.Model):
    """Даты повторения предметов."""

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="repeat_dates")
    date = models.DateTimeField("Дата и время начала")

    class Meta:
        verbose_name = "повторяющаяся дата предмета"
        verbose_name_plural = "повторяющиеся даты предметов"
        indexes = [
            models.Index(fields=["date"]),
        ]

    def __str__(self):
        return f"Дата повторения: {self.date} для предмета с ID {self.subject}"


class ScheduleAnchor(models.Model):
    start_date = models.DateField("Дата начала учебного семестра", default=datetime.date.today)
    end_date = models.DateField("Дата окончания учебного семестра", default=default_end_date)
    week_type = models.CharField(
        max_length=20,
        choices=FILTER_TYPE_OF_WEEK_CHOICES,
        verbose_name="Тип недели (Ч/З) в день начала занятий",
        default=NUMERATOR,
    )

    class Meta:
        verbose_name = "опорная дата расписания"
        verbose_name_plural = "опорная дата расписания"

    def __str__(self):
        # Словарь для перевода дней недели
        weekdays_translation = {
            "Monday": MONDAY,
            "Tuesday": TUESDAY,
            "Wednesday": WEDNESDAY,
            "Thursday": THURSDAY,
            "Friday": FRIDAY,
            "Saturday": SATURDAY,
            "Sunday": SUNDAY,
        }

        weekday_en = self.start_date.strftime("%A")
        weekday_ru = weekdays_translation.get(weekday_en, weekday_en)
        return f"{self.start_date} ({weekday_ru}) — {self.week_type}"
