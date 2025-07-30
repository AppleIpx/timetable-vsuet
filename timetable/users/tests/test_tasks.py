import pytest
from celery.result import EagerResult

from timetable.users.tasks import get_users_count
from timetable.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_user_count(settings):
    """
    Основной тест для выполнения задачи селери get_users_count.
    +1 потому что в миграции users 0007 создается суперпользователь и
    общее кол-во пользователей = 4
    """
    batch_size = 3
    UserFactory.create_batch(batch_size)
    settings.CELERY_TASK_ALWAYS_EAGER = True
    task_result = get_users_count.delay()
    users_count = batch_size + 1
    assert isinstance(task_result, EagerResult)
    assert task_result.result == users_count
