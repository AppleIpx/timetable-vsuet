def validate_subject_name_type_class(data_subject: str) -> tuple[str, str]:
    if ":" in data_subject:
        type_class, subject_name = map(str.strip, data_subject.split(":", 1))
        return type_class, subject_name
    return "практика", data_subject[0].strip()
