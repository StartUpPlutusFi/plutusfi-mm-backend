from numpy import require
from rest_framework import serializers
from apps.dashboard.db.models import *


class MMBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketMakerBot
        fields = "__all__"


class MMBotSerializerDetail(serializers.Serializer):
    class Meta:
        fields = ("id",)


class MMBotSerializerUpdate(serializers.Serializer):

    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)

    api_key = serializers.IntegerField(required=False)
    pair_token = serializers.IntegerField(required=False)

    trade_qty_range_low = serializers.IntegerField(required=False)
    trade_qty_range_high = serializers.IntegerField(required=False)
    trade_candle = serializers.IntegerField(required=False)
    trade_amount = serializers.FloatField(required=False)

    class Meta:
        fields = (
            "name",
            "description",
            "api_key",
            "pair_token",
            "trade_qty_range_low",
            "trade_qty_range_high",
            "trade_candle",
            "trade_amount",
        )

    def update(self, instance, validation_data):
        try:
            for k, v in validation_data.items():
                setattr(instance, k, v)
            instance.save()
            return instance

        except Exception:
            return None
