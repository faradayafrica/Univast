# Generated by Django 4.1.1 on 2023-09-02 00:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("academia", "0024_lecturetimetable_programme"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lecturetimetable",
            name="programme",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="academia.programme"
            ),
        ),
    ]
