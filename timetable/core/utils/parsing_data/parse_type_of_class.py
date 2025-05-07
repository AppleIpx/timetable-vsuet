def get_type_of_class(prepared_line: str) -> tuple[str, str]:
    if ":" in prepared_line:
        lesson_type, rest = map(str.strip, prepared_line.split(":", 1))
    else:
        lesson_type = "практические занятия"
        rest = prepared_line
    return lesson_type, rest
