from django.db.models.signals import post_delete
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Student
from .models import Teacher
from .utils.create_users_in_signals import create_person_in_users_signals


@receiver(pre_save, sender=Teacher)
def ensure_user_before_save_teacher(sender, instance, **kwargs):
    """Сигнал по созданию пользователя для преподавателей"""
    if instance.user is None:
        instance.user, instance.password = create_person_in_users_signals(instance, role="teacher")


@receiver(pre_save, sender=Student)
def ensure_user_before_save_student(sender, instance, **kwargs):
    """Сигнал по созданию пользователя для студента"""
    if instance.user is None:
        instance.user, instance.password = create_person_in_users_signals(instance, role="student")


@receiver(post_delete, sender=Teacher)
def delete_teacher_user(sender, instance, **kwargs):
    """Сигнал, который удаляет пользователя при удалении преподавателя"""
    if instance.user:
        instance.user.delete()


@receiver(post_delete, sender=Student)
def delete_student_user(sender, instance, **kwargs):
    """Сигнал, который удаляет пользователя при удалении студента"""
    if instance.user:
        instance.user.delete()
