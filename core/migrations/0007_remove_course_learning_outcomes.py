# Generated by Django 5.1.4 on 2025-01-16 11:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_course_hours_course_minutes_course_seconds_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='learning_outcomes',
        ),
    ]
