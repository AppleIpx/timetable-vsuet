from celery import shared_task

from timetable.core.models import Subject
from timetable.core.service.subject_repeat_service import SubjectRepeatService


@shared_task
def create_subject_repeat_dates_task(subject_id):
    """Таска для генерации повторяющихся дат."""
    subject = Subject.objects.get(id=subject_id)
    SubjectRepeatService(subject=subject)()
