# Generated by Django 4.1 on 2022-08-29 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("autotrade", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="marketmakerbot",
            name="pair_token",
            field=models.CharField(default="DUMMY", max_length=64),
        ),
    ]
