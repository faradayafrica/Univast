# Generated by Django 4.1.1 on 2023-09-02 00:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("academia", "0023_course_lecturetimetable"),
    ]

    operations = [
        migrations.AddField(
            model_name="lecturetimetable",
            name="programme",
            field=models.ForeignKey(
                default="0",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="program_timetables",
                to="academia.programme",
            ),
        ),
    ]
