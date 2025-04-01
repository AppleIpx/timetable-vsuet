from timetable.core.models import Audience


def create_auds(auds_data: list[str]) -> None:
    existing_auds = set(Audience.objects.values_list("name", flat=True))
    new_auds = [Audience(name=name) for name in auds_data if name not in existing_auds]

    Audience.objects.bulk_create(new_auds)
