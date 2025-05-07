from timetable.core.models import Group


def create_groups(groups_data: list[str]) -> None:
    existing_groups = set(Group.objects.values_list("name", flat=True))
    new_groups = [Group(name=name) for name in groups_data if name not in existing_groups]
    Group.objects.bulk_create(new_groups)
