from celery.app import shared_task

from timetable.utils.parsing_data import parse_data


@shared_task
def update_timetable():
    parse_data()
