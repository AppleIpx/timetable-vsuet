from django.conf import settings

from django.db import migrations


def create_superuser(apps, schema_editor):
    from django.contrib.auth import get_user_model

    User = get_user_model()
    username = settings.DJANGO_SUPERUSER_USERNAME
    email = settings.DJANGO_SUPERUSER_EMAIL
    password = settings.DJANGO_SUPERUSER_PASSWORD

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0006_alter_student_password_alter_teacher_password"),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
