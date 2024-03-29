# Generated by Django 4.1.1 on 2023-09-23 18:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("academia", "0025_alter_lecturetimetable_programme"),
    ]

    operations = [
        migrations.AddField(
            model_name="school",
            name="requests",
            field=models.IntegerField(
                blank=True,
                default=0,
                help_text="The number of requests submitted to make this School available on Faraday",
                null=True,
            ),
        ),
    ]
