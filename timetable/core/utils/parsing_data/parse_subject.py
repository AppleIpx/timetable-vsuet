def get_subject_name(parts: list[str], group_index: int) -> str:
    return " ".join(parts[: group_index - 3])
