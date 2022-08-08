# Generated by Django 4.0.6 on 2022-08-01 17:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ApiKeys",
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
                ("api_key", models.CharField(max_length=200, verbose_name="API KEY")),
                (
                    "api_secret",
                    models.CharField(max_length=200, verbose_name="API SECRET"),
                ),
                (
                    "description",
                    models.CharField(max_length=255, verbose_name="Description"),
                ),
                ("default", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "api_keys_store",
            },
        ),
        migrations.CreateModel(
            name="BidBot",
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
                ("name", models.CharField(default="None", max_length=32)),
                ("description", models.CharField(default="None", max_length=256)),
                ("order_size", models.IntegerField(default=0)),
                ("number_of_orders", models.IntegerField(default=0)),
                ("budget", models.FloatField(default=0)),
                ("trade_amount", models.FloatField(default=0)),
                ("status", models.CharField(default="STOP", max_length=16)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "api_key",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="dashboard.apikeys",
                    ),
                ),
            ],
            options={
                "db_table": "market_maker_bid_bot",
            },
        ),
        migrations.CreateModel(
            name="BotConfigPairtokens",
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
                ("pair", models.CharField(max_length=20, verbose_name="token")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "bot_config_pairtokens",
            },
        ),
        migrations.CreateModel(
            name="Exchenge",
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
                ("name", models.CharField(max_length=200)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="MarketMakerBot",
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
                ("name", models.CharField(max_length=32)),
                ("description", models.CharField(max_length=256)),
                ("trade_qty_range_low", models.IntegerField(default=0)),
                ("trade_qty_range_high", models.IntegerField(default=0)),
                ("trade_candle", models.IntegerField(default=10)),
                ("trade_amount", models.FloatField(default=0)),
                ("status", models.CharField(default="STOP", max_length=16)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "api_key",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="dashboard.apikeys",
                    ),
                ),
                (
                    "pair_token",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="dashboard.botconfigpairtokens",
                        verbose_name="Token pair",
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
            options={
                "db_table": "market_maker_bot",
            },
        ),
        migrations.CreateModel(
            name="MarketMakerBotOrderHistory",
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
                ("spreed", models.IntegerField(default=0)),
                ("status", models.CharField(default="STOP", max_length=16)),
                ("side", models.CharField(max_length=4)),
                ("trade_qty_low", models.IntegerField(default=0)),
                ("trade_qty_high", models.IntegerField(default=0)),
                ("trade_candle", models.IntegerField(default=0)),
                ("trade_amount", models.FloatField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "bot",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="dashboard.marketmakerbot",
                    ),
                ),
            ],
            options={
                "db_table": "market_maker_bot_order_history",
            },
        ),
        migrations.CreateModel(
            name="DashboardSysLogs",
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
                ("action", models.CharField(max_length=64)),
                ("data", models.TextField(max_length=256)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "dashboard_sys_logs",
            },
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
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="dashboard.marketmakerbot",
                    ),
                ),
            ],
            options={
                "db_table": "cancel_order_book_mm_bot",
            },
        ),
        migrations.CreateModel(
            name="CancelOrderBookBID",
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
                ("cancel_order_list", models.CharField(max_length=512)),
                ("order_status", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "bid_bot",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="dashboard.bidbot",
                    ),
                ),
            ],
            options={
                "db_table": "cancel_order_book_bid_bot",
            },
        ),
        migrations.CreateModel(
            name="BidBotOrderHistory",
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
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="dashboard.bidbot",
                    ),
                ),
            ],
            options={
                "db_table": "bid_bot_order_history",
            },
        ),
        migrations.AddField(
            model_name="bidbot",
            name="pair_token",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="dashboard.botconfigpairtokens",
                verbose_name="Token pair",
            ),
        ),
        migrations.AddField(
            model_name="bidbot",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="apikeys",
            name="exchange",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="dashboard.exchenge",
            ),
        ),
        migrations.AddField(
            model_name="apikeys",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
