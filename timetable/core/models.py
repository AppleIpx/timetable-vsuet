from django.db import models

from timetable.core.enums import TypeOfClass, TypeOfWeek, TypeOfDay
from timetable.users.models import Teacher


class Faculty(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "факультет"
        verbose_name_plural = "факультеты"

    def __str__(self):
        return f"факультет {self.name}"


class Group(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "группа"
        verbose_name_plural = "группы"

    def __str__(self):
        return self.name


class TimeSubject(models.Model):
    number = models.PositiveSmallIntegerField(unique=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        verbose_name = "время пары"
        verbose_name_plural = "время пар"

    def __str__(self):
        return f"{self.number}: {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    audience = models.CharField(max_length=50)

    type_of_day = models.CharField(
        max_length=15,
        choices=[(tag.value, tag.name) for tag in TypeOfDay],
    )

    type_of_week = models.CharField(
        max_length=15,
        choices=[(tag.value, tag.name) for tag in TypeOfWeek],
    )
    type_of_classes = models.CharField(
        max_length=10,
        choices=[(tag.value, tag.name) for tag in TypeOfClass],
    )
    time_subject = models.ForeignKey(TimeSubject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "предмет"
        verbose_name_plural = "предметы"

    def __str__(self):
        return self.name
