import logging

import httpx
from bs4 import BeautifulSoup
from bs4.element import Tag

from config.settings.base import env
from timetable.core.utils import create_auds
from timetable.core.utils import create_groups
from timetable.core.utils.create_subjects import create_subjects
from timetable.users.utils import create_teachers


def fetch_page(
    url: str,
    type_of_http: str,
    form_data: dict[str, str] | None = None,
) -> str:
    try:
        with httpx.Client(timeout=10) as client:
            if type_of_http == "get":
                response = client.get(url)
            elif type_of_http == "post":
                response = client.post(url, data=form_data)
            else:
                msg_error = f"Unsupported HTTP method: {type_of_http}"
                raise ValueError(msg_error)  # noqa: TRY301
            response.raise_for_status()
            return response.text

    except (httpx.HTTPStatusError, httpx.RequestError, ValueError) as e:
        msg_error = f"When performing a request, an error occurred, {url}: {e}"
        logging.exception(msg_error)
        return ""


def parse_timetable(type_of_day: str) -> None:
    url = env("TIMETABLE_URL")
    html = fetch_page(
        url=url,
        type_of_http="post",
        form_data={
            "select_dow": f"{type_of_day}",
        },
    )
    soup = BeautifulSoup(html, "html.parser")
    all_subjects = soup.find_all(
        "table",
        {"class": "table table-hover table-bordered table-sm"},
    )
    if len(all_subjects) == 0:
        warning_msg = f"No subjects were found for {type_of_day}"
        logging.warning(warning_msg)
        return
    create_subjects(all_subjects)


def collect_data(data: Tag | None) -> list[str]:
    if data is None:
        msg_error = "data must be provided."
        raise ValueError(msg_error)
    options = data.find_all("option")
    return [option.text.strip() for option in options if option.text.strip()]


def parse_data() -> None:
    url = env("TIMETABLE_URL")
    html = fetch_page(url=url, type_of_http="get")
    days = ["ПОНЕДЕЛЬНИК", "ВТОРНИК", "СРЕДА", "ЧЕТВЕРГ", "ПЯТНИЦА", "СУББОТА"]
    soup = BeautifulSoup(html, "html.parser")

    teachers_tag = soup.find(
        "select",
        {"name": "select_prepod", "class": "form-select"},
    )
    groups_tag = soup.find("select", {"name": "select_group", "class": "form-select"})
    aud_tag = soup.find("select", {"name": "select_aud", "class": "form-select"})

    teachers_data = collect_data(teachers_tag)  # type:ignore[arg-type]
    groups_data = collect_data(groups_tag)  # type:ignore[arg-type]
    auds_data = collect_data(aud_tag)  # type:ignore[arg-type]

    create_teachers(teachers_data=teachers_data)
    create_groups(groups_data=groups_data)
    create_auds(auds_data=auds_data)
    for day in days:
        parse_timetable(type_of_day=day)
