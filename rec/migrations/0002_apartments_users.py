# Generated by Django 4.1 on 2023-02-22 09:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("rec", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="apartments",
            name="users",
            field=models.ManyToManyField(
                related_name="apartments", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
