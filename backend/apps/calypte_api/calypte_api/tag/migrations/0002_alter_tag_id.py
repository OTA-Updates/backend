# Generated by Django 5.0.2 on 2024-02-20 16:12

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tag", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tag",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
    ]
