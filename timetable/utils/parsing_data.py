import logging

import httpx
from bs4 import BeautifulSoup
from bs4.element import Tag

from config.settings.base import env
from timetable.core.utils import create_auds
from timetable.core.utils import create_groups
from timetable.users.utils import create_teachers


def fetch_page(url: str) -> str:
    try:
        with httpx.Client(timeout=10) as client:
            response = client.get(url)
            response.raise_for_status()
            return response.text
    except (httpx.HTTPStatusError, httpx.RequestError) as e:
        msg_error = f"When performing a request, an error occurred, {url}: {e}"
        logging.exception(msg_error)
        return ""


def collect_data(data: Tag | None) -> list[str]:
    if data is None:
        msg_error = "data must be provided."
        raise ValueError(msg_error)
    options = data.find_all("option")
    return [option.text.strip() for option in options if option.text.strip()]


def parse_data() -> None:
    url = env("TIMETABLE_URL")
    html = fetch_page(url)

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
