# Generated by Django 4.1 on 2022-08-25 12:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("exchange", "0001_initial"),
        ("autotrade", "__first__"),
    ]

    operations = [
        migrations.CreateModel(
            name="BookFiller",
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
                ("name", models.CharField(default="nil", max_length=32)),
                ("side", models.CharField(default="nil", max_length=5)),
                ("pair_token", models.CharField(default="DUMMy", max_length=8)),
                ("order_size", models.IntegerField(default=0)),
                ("number_of_orders", models.IntegerField(default=0)),
                ("budget", models.FloatField(default=0)),
                ("user_ref_price", models.FloatField(default=0)),
                ("status", models.CharField(default="STOP", max_length=16)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "api_key",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="exchange.apikeys",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CancelOrderBookBot",
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
                ("cancel_order_id", models.CharField(max_length=64)),
                ("order_status", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "bot",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="autotrade.marketmakerbot",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BookFillerOrderHistory",
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
                ("pair_token", models.CharField(default="DUMMY_TK", max_length=16)),
                ("order_size", models.IntegerField(default=0)),
                ("number_of_orders", models.IntegerField(default=0)),
                ("budget", models.FloatField(default=0)),
                ("trade_amount", models.FloatField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "bid_bot",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="bookfiller.bookfiller",
                    ),
                ),
            ],
        ),
    ]