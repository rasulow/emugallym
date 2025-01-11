# Generated by Django 5.1.4 on 2025-01-11 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_user_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='type',
            field=models.CharField(blank=True, choices=[('instructor', 'Instructor'), ('student', 'Student')], max_length=10, null=True),
        ),
    ]
