# Generated by Django 4.1.1 on 2023-05-14 12:39

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("academia", "0012_remove_school_listed_school_unlisted"),
    ]

    operations = [
        migrations.AlterField(
            model_name="school",
            name="logo",
            field=cloudinary.models.CloudinaryField(
                default="logo.png",
                help_text="The logo of this institution",
                max_length=255,
                verbose_name="univast-school-logos",
            ),
        ),
    ]
