from django.db import models


def get_audience(
    parts: list[str],
    group_index: int,
    db_cache: dict[str, dict[str, models.Model]],
) -> str:
    """
    Извлекает аудиторию из parts[group_index - 1]
    Удаляет один префикс "a." если он есть. Проверяет наличие в БД.
    """
    audience_db = db_cache["audiences"]
    audience_raw = parts[group_index - 1]

    audience_clean = audience_raw[2:] if audience_raw.startswith("а.") else audience_raw

    if audience_clean in audience_db:
        return audience_clean

    return audience_raw
