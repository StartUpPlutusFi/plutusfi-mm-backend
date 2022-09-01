from django.db import models

from apps.account.models import User
from apps.exchange.models.models import ApiKeys


class Geneses(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    api_key = models.ForeignKey(ApiKeys, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=200)
    token = models.CharField(max_length=64)
    user_order_size_bid = models.FloatField(default=0)
    user_order_size_ask = models.FloatField(default=0)
    market_value = models.FloatField(default=0)
    spread_distance = models.FloatField(default=0)
    status = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class GenesesQueue(models.Model):
    geneses_id = models.ForeignKey(Geneses,  on_delete=models.DO_NOTHING)
    cancel_code = models.CharField(max_length=128)
    status = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cancel_code

