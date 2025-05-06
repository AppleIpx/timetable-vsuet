import logging
from datetime import datetime
from datetime import time

from bs4.element import ResultSet
from bs4.element import Tag
from django.db import models

from timetable.core.models import Audience
from timetable.core.models import ErrorSubject
from timetable.core.models import Group
from timetable.core.models import Subject
from timetable.core.models import TimeSubject
from timetable.core.utils.parsing_data.parse_subject_table import parse_line_flexible
from timetable.core.utils.validators.professor_name import validate_teacher_name
from timetable.users.models import Teacher


class CollectDataError(Exception):
    def __init__(self, message: str, partial_data: dict[str, models.Model | str]):
        super().__init__(message)
        self.partial_data = partial_data


def transformation_string_time(
    string_time: str,
) -> time:
    time_subject_str = string_time.strip()
    return datetime.strptime(time_subject_str.split("-")[0], "%H.%M").time()


def get_data(
    data_subject_tag: Tag,
    data_day: ResultSet,
    db_cache: dict[str, dict[str, models.Model]],
) -> dict[str, str]:
    # type_class, subject_name = validate_subject_name_type_class(data_subject[0])
    # professor_name = validate_professor_name(
    #     professor_name=data_subject[1].find(
    #         "div",
    #         {"class": "box_rounded link_prepod px-3"},
    #     ).text,
    #     data_subject_tag=data_subject_tag.text,
    #     db_cache=db_cache
    # )
    # audience, group = validate_audience_and_group(data=data_subject[2].text)
    parsed_data = parse_line_flexible(
        line=data_subject_tag.text,
        db_cache=db_cache,
    )
    validate_teacher_name(
        teacher_name=parsed_data["teacher"],
        db_cache=db_cache,
    )
    subgroup = check_subgroup(data=parsed_data, db_cache=db_cache)
    return {
        "type_of_classes": parsed_data["type_of_classes"],
        "subject_name": parsed_data["subject_name"],
        "teacher": parsed_data["teacher"],
        "type_of_day": data_day[0].text,
        "time_subject": transformation_string_time(data_day[1].text),
        "type_of_week": data_day[2].text,
        "audience": parsed_data["audience"],
        "group": parsed_data["group"],
        "subgroup": subgroup,
    }


def preload_db_data() -> dict[str, dict[str, models.Model]]:
    return {
        "times": {t.start_time: t for t in TimeSubject.objects.all()},
        "teachers": {t.full_name: t for t in Teacher.objects.all()},
        "audiences": {a.name: a for a in Audience.objects.all()},
        "groups": {g.name: g for g in Group.objects.all()},
    }


def check_subgroup(
    data: dict[str, str],
    db_cache: dict[str, dict[str, models.Model]],
) -> int:
    if Subject.objects.filter(
        name=data["subject_name"],
        subgroup=1,
        group=db_cache["groups"].get(data["group"]),
    ).exists():
        return 2
    return 1


def save_subject(subject_data: dict[str, models.Model | str]) -> None:
    obj, created = Subject.objects.update_or_create(
        name=subject_data["subject_name"],
        defaults={
            "audience": subject_data["audience"],
            "type_of_day": subject_data["type_of_day"],
            "type_of_week": subject_data["type_of_week"],
            "type_of_classes": subject_data["type_of_classes"],
            "time_subject": subject_data["time_subject"],
            "teacher": subject_data["teacher"],
            "group": subject_data["group"],
            "subgroup": subject_data["subgroup"],
        },
    )
    if created:
        logging.info(f"Created new subject: {obj.name}")
    else:
        logging.info(f"Updated existing subject: {obj.name}")


def validate_objects(
    data: dict[str, str],
    db_cache: dict[str, dict[str, models.Model]],
) -> dict[str, models.Model | str]:
    """
    Проверяет наличие нужных объектов в кэше.
    Если что-то не найдено — собирает возможные данные и выбрасывает CollectDataError.
    """

    def _collect_base_data() -> dict[str, models.Model | str]:
        return {
            "subject_name": data.get("subject_name"),
            "type_of_day": data.get("type_of_day"),
            "type_of_week": data.get("type_of_week"),
            "type_of_classes": data.get("type_of_classes"),
            "subgroup": data.get("subgroup"),
        }

    db_cache["teachers"] = {t.full_name: t for t in Teacher.objects.all()}
    validated_data = {}
    key_map = {
        "audience": "audiences",
        "group": "groups",
        "time_subject": "times",
        "teacher": "teachers",
    }

    for data_key, cache_key in key_map.items():
        value = data[data_key]
        obj = db_cache[cache_key].get(value)
        if obj:
            validated_data[data_key] = obj
        else:
            logging.warning(f"В БД не найдено значение для '{data_key}': {value}")
            validated_data.update(_collect_base_data())
            raise CollectDataError(
                f"Collect Data Error: '{data_key}' with value '{value}' not found in DB cache.",
                partial_data=validated_data,
            )

    validated_data.update(_collect_base_data())
    return validated_data


def validate_data(
    subject: Tag,
    db_cache: dict[str, dict[str, models.Model]],
) -> dict[str, models.Model | str]:
    data_day = subject.find_all("th", {"class": "align-middle"})
    # data_subject_content = subject.find("td", {"class": "align-middle"}).contents
    data_subject_tag = subject.find("td", {"class": "align-middle"})
    parsed_data = get_data(
        data_day=data_day,
        # data_subject_content=data_subject_content,
        data_subject_tag=data_subject_tag,
        db_cache=db_cache,
    )
    return validate_objects(data=parsed_data, db_cache=db_cache)


def create_subjects(all_subjects: ResultSet) -> None:
    db_cache = preload_db_data()
    for subject in all_subjects:
        try:
            validated_data = validate_data(subject=subject, db_cache=db_cache)
            save_subject(subject_data=validated_data)
        except CollectDataError as e:
            partial = e.partial_data
            msg_error = f"Ошибка валидации при парсинге предмета: {e}"
            logging.exception(msg_error)
            print("ababababa", partial)

            ErrorSubject.objects.create(
                name=partial.get("subject_name"),
                audience=partial.get("audience"),
                type_of_day=partial.get("type_of_day"),
                type_of_week=partial.get("type_of_week"),
                type_of_classes=partial.get("type_of_classes"),
                time_subject=partial.get("time_subject"),
                teacher=partial.get("teacher"),
                group=partial.get("group"),
                subgroup=partial.get("subgroup"),
                cause_of_error=str(e),
            )
        except Exception as e:
            logging.exception(f"Неизвестная ошибка при парсинге предмета: {e}")
