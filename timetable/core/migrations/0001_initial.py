# Generated by Django 5.0.13 on 2025-03-25 21:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'факультет',
                'verbose_name_plural': 'факультеты',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'группа',
                'verbose_name_plural': 'группы',
            },
        ),
        migrations.CreateModel(
            name='TimeSubject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveSmallIntegerField(unique=True)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
            ],
            options={
                'verbose_name': 'время пары',
                'verbose_name_plural': 'время пар',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('audience', models.CharField(max_length=50)),
                ('type_of_day', models.CharField(choices=[('monday', 'MONDAY'), ('tuesday', 'TUESDAY'), ('wednesday', 'WEDNESDAY'), ('thursday', 'THURSDAY'), ('friday', 'FRIDAY'), ('saturday', 'SATURDAY')], max_length=15)),
                ('type_of_week', models.CharField(choices=[('numerator', 'NUMERATOR'), ('denominator', 'DENOMINATOR')], max_length=15)),
                ('type_of_classes', models.CharField(choices=[('lecture', 'LECTURE'), ('practice', 'PRACTICE'), ('laboratory', 'LABORATORY')], max_length=10)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.faculty')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.group')),
            ],
            options={
                'verbose_name': 'предмет',
                'verbose_name_plural': 'предметы',
            },
        ),
    ]
