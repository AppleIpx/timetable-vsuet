from django.db import models

from timetable.core.utils.parsing_data.parse_audience import get_audience
from timetable.core.utils.parsing_data.parse_group import get_group
from timetable.core.utils.parsing_data.parse_subject import get_subject_name
from timetable.core.utils.parsing_data.parse_teacher import get_teacher_name
from timetable.core.utils.parsing_data.parse_type_of_class import get_type_of_class
from timetable.core.utils.parsing_data.prepare_line import prepare_prepare_line


def parse_line_flexible(
    line: str,
    db_cache: dict[str, dict[str, models.Model]],
) -> dict[str, str]:
    prepared_line = prepare_prepare_line(line=line)
    type_class, rest = get_type_of_class(prepared_line=prepared_line)
    parts = rest.split()
    group, group_index = get_group(parts=parts)
    audience = get_audience(
        parts=parts,
        group_index=group_index,
        db_cache=db_cache,
    )
    teacher = get_teacher_name(parts=parts, group_index=group_index)
    subject = get_subject_name(parts=parts, group_index=group_index)

    return {
        "type_of_classes": type_class,
        "subject_name": subject,
        "teacher": teacher,
        "audience": audience,
        "group": group,
    }
