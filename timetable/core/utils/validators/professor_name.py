from django.db import models

from timetable.users.models import Teacher


def validate_teacher_name(
    teacher_name: str,
    db_cache: dict[str, dict[str, models.Model]],
) -> str | None:
    if db_cache["teachers"].get(f"{teacher_name}") is None:
        Teacher.objects.get_or_create(full_name=teacher_name)
        return teacher_name
    return None
