# Generated by Django 4.1 on 2022-10-10 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rec", "0005_alter_priceinfo_options_priceinfo_per_price_and_more"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="priceinfo",
            constraint=models.UniqueConstraint(
                fields=("apart", "date"), name="unique aprart price"
            ),
        ),
    ]
