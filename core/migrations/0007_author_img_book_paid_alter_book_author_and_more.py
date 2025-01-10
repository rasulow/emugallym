# Generated by Django 5.1.4 on 2025-01-10 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_tag_remove_book_discount_remove_book_price_book_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='authors/'),
        ),
        migrations.AddField(
            model_name='book',
            name='paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ManyToManyField(blank=True, null=True, to='core.author'),
        ),
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(blank=True, null=True, to='core.genre'),
        ),
        migrations.AlterField(
            model_name='book',
            name='tag',
            field=models.ManyToManyField(blank=True, null=True, to='core.tag'),
        ),
    ]
