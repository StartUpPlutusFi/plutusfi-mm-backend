from rest_framework import serializers
from apps.autotrade.models.models import *


class MMBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketMakerBot
        fields = "__all__"


class MMBotSerializerDetail(serializers.Serializer):
    class Meta:
        fields = ("id",)


class MMBotSerializerAdd(serializers.Serializer):
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    api_key_id = serializers.IntegerField(required=True)
    user_id = serializers.IntegerField(required=True)
    pair_token = serializers.CharField(required=False)
    user_ref_price = serializers.FloatField(required=False)
    trade_candle = serializers.IntegerField(required=False)
    trade_amount = serializers.FloatField(required=False)


    class Meta:
        fields = (
            "id",
            "name",
            "description",
            "api_key_id",
            "user_id",
            "pair_token",
            "user_ref_price",
            "trade_candle",
            "trade_amount",
        )

    def create(self, validated_data):
        return MarketMakerBot.objects.create(**validated_data)


class MMBotSerializerUpdate(serializers.Serializer):
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)

    api_key_id = serializers.IntegerField(required=False)
    pair_token = serializers.IntegerField(required=False)

    trade_qty_range_low = serializers.IntegerField(required=False)
    trade_qty_range_high = serializers.IntegerField(required=False)
    trade_candle = serializers.IntegerField(required=False)
    trade_amount = serializers.FloatField(required=False)

    class Meta:
        fields = (
            "name",
            "description",
            "api_key_id",
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


class MMBotSerializerStatus(serializers.Serializer):
    status = serializers.CharField()

    class Meta:
        fields = ("status",)

    def update(self, instance, validation_data):
        try:
            for k, v in validation_data.items():
                setattr(instance, k, v)
            instance.save()
            return instance

        except Exception:
            return None
