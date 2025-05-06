import logging
import re


def validate_audience_and_group(data: str):
    cleaned_data = re.sub(r"\s+", " ", data).strip()
    pattern = r"\(?а\.\s*(\d+[а-яА-Я]?)\)?[,;]?\s*гр\.\s*([\w-]+)"
    match = re.search(pattern, cleaned_data, re.IGNORECASE)

    if not match:
        msg = f"Невозможно извлечь аудиторию и группу из строки: {data}"
        logging.error(msg)
    try:
        return match.group(1), match.group(2)
    except AttributeError:
        logging.exception(
            f"При парсинге аудитории и группы произошла ошибка, исходные данные: {data}",
        )
        return "", ""
