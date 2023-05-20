# Generated by Django 4.1.1 on 2023-05-18 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academia', '0018_alter_clientapikey_expiry_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientapikey',
            name='rate',
            field=models.BigIntegerField(default=60, help_text='Default throttle rate for requests per hour.'),
        ),
    ]
