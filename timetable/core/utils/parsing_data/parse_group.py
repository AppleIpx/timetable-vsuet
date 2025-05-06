def get_group(parts: list[str]) -> tuple[str, int] | None:
    group_index = next(
        (i for i, part in enumerate(parts) if part.startswith("гр.")),
        None,
    )
    if group_index is None or group_index < 3:  # noqa: PLR2004
        return None

    return parts[group_index].replace("гр.", ""), group_index
