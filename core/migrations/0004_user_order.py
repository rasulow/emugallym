# Generated by Django 5.1.4 on 2025-01-11 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='order',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
