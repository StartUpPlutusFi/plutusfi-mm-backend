from django.db import models
from apps.exchange.models.models import ApiKeys
from apps.account.models import User


# Create your models here.


class OrderLimit(models.Model):
    name = models.CharField(max_length=32, default="nil")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    api_key = models.ForeignKey(ApiKeys, on_delete=models.DO_NOTHING)
    side = models.CharField(max_length=5, default="nil")
    pair_token = models.CharField(max_length=64, default="DUMMY")
    quantity = models.FloatField(default=0)
    price = models.FloatField(default=0)
    status = models.CharField(max_length=16, default="STOP")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class OrderLimitOrderHistory(models.Model):
    OrderLimitCfg = models.ForeignKey(OrderLimit, models.DO_NOTHING)
    side = models.CharField(max_length=5, default="nil")
    pair_token = models.CharField(max_length=64, default="DUMMY")
    quantity = models.FloatField(default=0)
    price = models.FloatField(default=0)
    trade_amount = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class CancelOrderOrderLimit(models.Model):
    OrderLimitCfg = models.ForeignKey(OrderLimit, models.DO_NOTHING)
    cancel_order_id = models.CharField(max_length=64)
    order_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.cancel_order_id)
