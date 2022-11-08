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
    photo = serializers.ImageField(required=False)
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=False)
    api_key_id = serializers.IntegerField(required=True)
    user_id = serializers.IntegerField(required=False)
    pair_token = serializers.CharField(required=True)
    user_ref_price = serializers.FloatField(required=True)
    trade_candle = serializers.IntegerField(required=True)
    trade_amount = serializers.FloatField(required=True)

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
        new_autotrade = MarketMakerBot.objects.create( user=self.context["request"].user, **validated_data)
        new_autotrade.save()
        return new_autotrade


class MMBotSerializerUpdate(serializers.Serializer):
    photo = serializers.ImageField(required=False)
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=False)
    user_id = serializers.IntegerField(required=False)
    pair_token = serializers.CharField(required=True)
    user_ref_price = serializers.FloatField(required=True)
    trade_candle = serializers.IntegerField(required=True)
    trade_amount = serializers.FloatField(required=True)

    class Meta:
        fields = (
            "id",
            "name",
            "description",
            "user_id",
            "pair_token",
            "user_ref_price",
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


class MMBotSerializerResponse(serializers.ModelSerializer):
    class Meta:
        model = MarketMakerBot
        exclude = ("user",)