import logging

from django.db import transaction
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver
from kombu import Connection

from config import celery_app
from timetable.core.constant import UPDATE_REPEAT_DATE_FIELDS
from timetable.core.models import Subject
from timetable.core.tasks import create_subject_repeat_dates_task

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Subject)
def set_subject_init_values(sender, instance, *args, **kwargs):
    """
    Сохраняет начальные значения полей повтора перед сохранением объекта Subject.

    Если объект уже существует (обновление), сохраняет исходные значения указанных полей
    в атрибутах вида init_<поле> и копирует старое состояние в _old_state.
    Используется для отслеживания изменений в логике повтора.
    """
    init_values = dict.fromkeys(UPDATE_REPEAT_DATE_FIELDS)

    if instance.id:
        old_subject = Subject.objects.get(pk=instance.id)
        for key in init_values:
            init_values[key] = getattr(old_subject, key)
        instance._old_state = old_subject  # noqa: SLF001

    for key, value in init_values.items():
        setattr(instance, f"init_{key}", value)


@receiver(post_save, sender=Subject)
def subject_post_save(sender, instance, created, **kwargs):
    """
    После сохранения Subject проверяет, изменились ли поля повтора,
    и при необходимости запускает Celery-задачу для создания/обновления повторяющихся записей.
    """

    def creating_repeat_subject():
        logger.info(
            "Creating subject repeat dates task. Event ID: %s. Celery config: broker_url=%s, transport=%s",
            instance.pk,
            celery_app.conf.broker_url,
            celery_app.conf.broker_transport,
        )
        allow_update = False
        for filed in UPDATE_REPEAT_DATE_FIELDS:
            if getattr(instance, filed) != getattr(instance, f"init_{filed}"):
                allow_update = True

        if not allow_update:
            return

        try:
            with Connection(celery_app.conf.broker_url, transport_options={"visibility_timeout": 3600}) as conn:
                result = create_subject_repeat_dates_task.apply_async(
                    args=[instance.pk],
                    connection=conn,
                    retry=True,
                    retry_policy={
                        "max_retries": 3,
                        "interval_start": 0.1,
                        "interval_step": 0.2,
                        "interval_max": 0.5,
                    },
                )
                logger.info("Subject created successfully. Task ID: %s", result.id)
        except Exception as e:
            logger.error(  # noqa: G201
                "Failed to create task for subject %s. Error: %s. Celery config: broker_url=%s, transport=%s",
                instance.pk,
                str(e),
                celery_app.conf.broker_url,
                celery_app.conf.broker_transport,
                exc_info=True,
            )

    transaction.on_commit(creating_repeat_subject)
