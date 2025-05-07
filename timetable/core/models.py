from django.db import models

from timetable.users.models import Teacher


class BaseModel(models.Model):
    name = models.CharField(max_length=100)

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
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        verbose_name = "время пары"
        verbose_name_plural = "время пар"

    def __str__(self):
        return f"пара {self.number}"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    audience = models.ForeignKey(
        Audience,
        null=True,
        on_delete=models.SET_NULL,
    )
    type_of_day = models.CharField(max_length=20, verbose_name="день недели")
    type_of_week = models.CharField(max_length=20, verbose_name="тип недели")
    type_of_classes = models.CharField(max_length=20, verbose_name="тип занятия")
    time_subject = models.ForeignKey(TimeSubject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    subgroup = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = "предмет"
        verbose_name_plural = "предметы"

    def __str__(self):
        return self.name


class ErrorSubject(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)  # noqa: DJ001
    audience = models.CharField(max_length=100, null=True, blank=True)  # noqa: DJ001
    type_of_day = models.CharField(  # noqa: DJ001
        max_length=20,
        verbose_name="день недели",
        blank=True,
        null=True,
    )
    type_of_week = models.CharField(  # noqa: DJ001
        max_length=20,
        verbose_name="тип недели",
        blank=True,
        null=True,
    )
    type_of_classes = models.CharField(  # noqa: DJ001
        max_length=20,
        verbose_name="тип занятия",
        blank=True,
        null=True,
    )
    time_subject = models.ForeignKey(
        TimeSubject,
        on_delete=models.CASCADE,
        default=1,
        blank=True,
        null=True,
    )
    teacher = models.CharField(blank=True, null=True, max_length=100)  # noqa: DJ001
    group = models.CharField(blank=True, null=True, max_length=100)  # noqa: DJ001
    subgroup = models.PositiveSmallIntegerField(blank=True, null=True)
    cause_of_error = models.TextField(null=True, blank=True)  # noqa: DJ001

    class Meta:
        verbose_name = "предмет с ошибкой"
        verbose_name_plural = "предметы с ошибками"

    def __str__(self):
        return self.name
