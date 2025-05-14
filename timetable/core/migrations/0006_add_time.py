import datetime

from django.db import migrations


def add_time_subjects(apps, schema_editor):
    TimeSubject = apps.get_model("core", "TimeSubject")
    time_data = [
        (1, datetime.time(8, 0), datetime.time(9, 45)),
        (2, datetime.time(9, 55), datetime.time(11, 20)),
        (3, datetime.time(11, 50), datetime.time(13, 25)),
        (4, datetime.time(13, 35), datetime.time(15, 10)),
        (5, datetime.time(15, 20), datetime.time(16, 55)),
        (6, datetime.time(17, 5), datetime.time(18, 40)),
        (7, datetime.time(18, 50), datetime.time(20, 25)),
    ]

    for number, start, end in time_data:
        TimeSubject.objects.create(number=number, start_time=start, end_time=end)


def remove_time_subjects(apps, schema_editor):
    TimeSubject = apps.get_model("core", "TimeSubject")
    TimeSubject.objects.filter(number__in=range(1, 8)).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_alter_subject_type_of_classes_and_more"),
    ]

    operations = [
        migrations.RunPython(add_time_subjects, remove_time_subjects),
    ]
