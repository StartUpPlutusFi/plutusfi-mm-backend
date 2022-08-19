# Generated by Django 4.1 on 2022-08-11 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0003_remove_marketmakerbot_trade_qty_range_high_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="MarketMakerBotAutoTradeQueue",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("price", models.FloatField(default=0)),
                ("quantity", models.IntegerField(default=0)),
                ("side", models.CharField(default="Nil")),
                ("status", models.CharField(default="FINISHED")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "bot",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="dashboard.marketmakerbot",
                    ),
                ),
            ],
        ),
    ]
