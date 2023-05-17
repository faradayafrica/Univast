# Generated by Django 4.1.1 on 2023-05-16 21:52

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("academia", "0014_client_clientapikey_client_clients_id_f1f4a8_idx"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
    ]