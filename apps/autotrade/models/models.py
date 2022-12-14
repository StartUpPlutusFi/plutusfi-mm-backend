from apps.exchange.models.models import *
from apps.account.models import User
from django.db import models
from django.conf import settings


class MarketMakerBot(models.Model):
    photo = models.ImageField(upload_to="images", blank=True)
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    api_key = models.ForeignKey(ApiKeys, on_delete=models.DO_NOTHING)
    pair_token = models.CharField(max_length=64, default="DUMMY")
    user_ref_price = models.FloatField(default=0)
    side = models.IntegerField(default=0)
    trade_candle = models.IntegerField(default=0)
    trade_amount = models.FloatField(default=0)
    status = models.CharField(max_length=8, default="STOP")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def api(self):
        return self.api_key.name

    def __str__(self):
        return self.name


class MarketMakerBotOrderHistory(models.Model):
    bot = models.ForeignKey(MarketMakerBot, models.DO_NOTHING)
    pair_token = models.CharField(max_length=64, default="DUMMY")
    user_ref_price = models.FloatField(default=0)
    exec_ref_price = models.FloatField(default=0)
    side = models.CharField(default="FILL", max_length=64)
    trade_candle = models.IntegerField(default=0)
    trade_amount = models.FloatField(default=0)
    status = models.CharField(default="FINISHED", max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.bot.id)


class MarketMakerBotAutoTradeQueue(models.Model):
    bot = models.ForeignKey(MarketMakerBot, models.DO_NOTHING)
    price = models.FloatField(default=0)
    exec_ref_price = models.FloatField(default=0)
    quantity = models.FloatField(default=0)
    side = models.CharField(default="FILL", max_length=64)
    status = models.CharField(default="FINISHED", max_length=64)
    candle = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.bot.id)
