from django.db import models

from timetable.core.enums import TYPE_OF_CLASSES_CHOICES
from timetable.core.enums import TYPE_OF_DAY_CHOICES
from timetable.core.enums import TYPE_OF_WEEK_CHOICES
from timetable.users.models import Teacher


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
    type_of_day = models.CharField(
        max_length=20,
        verbose_name="День недели",
        choices=TYPE_OF_DAY_CHOICES,
        default="",
    )
    type_of_week = models.CharField(
        max_length=20,
        verbose_name="Тип недели",
        choices=TYPE_OF_WEEK_CHOICES,
        default="",
    )
    type_of_classes = models.CharField(
        max_length=30,
        verbose_name="Тип занятия",
        choices=TYPE_OF_CLASSES_CHOICES,
        default="",
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
    )

    class Meta:
        verbose_name = "предмет"
        verbose_name_plural = "предметы"

    def __str__(self):
        return self.name
