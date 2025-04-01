from timetable.users.models import Teacher


def create_teachers(teachers_data: list[str]) -> None:
    existing_teachers = set(Teacher.objects.values_list("full_name", flat=True))
    new_teachers = [
        Teacher(
            full_name=name,
        )
        for name in teachers_data
        if name not in existing_teachers
    ]
    Teacher.objects.bulk_create(new_teachers)
