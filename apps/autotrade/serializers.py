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
    side = serializers.IntegerField(required=True)
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
            "side",
            "pair_token",
            "user_ref_price",
            "trade_candle",
            "trade_amount",
        )

    def create(self, validated_data):
        validated_data = validated_data | {
            "api_key_id": ApiKeys.objects.filter(
                id=validated_data["api_key_id"], user=self.context["request"].user
            )
            .values("id")
            .first()["id"],
        }
        new_autotrade = MarketMakerBot.objects.create(
            user=self.context["request"].user, **validated_data
        )
        new_autotrade.save()
        return new_autotrade


class MMBotSerializerUpdate(serializers.Serializer):
    photo = serializers.ImageField(required=False)
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    side = serializers.IntegerField(required=False)
    pair_token = serializers.CharField(required=False)
    user_ref_price = serializers.FloatField(required=False)
    trade_candle = serializers.IntegerField(required=False)
    trade_amount = serializers.FloatField(required=False)

    class Meta:
        fields = (
            "photo",
            "name",
            "description",
            "side",
            "pair_token",
            "user_ref_price",
            "trade_candle",
            "trade_amount",
        )

    def update(self, instance, validation_data):
        try:

            for k, v in validation_data.items():
                if k == "photo":
                    v = self.context["request"].data["photo"]
                if k == "api_key_id":
                    v = \
                        ApiKeys.objects.filter(id=validation_data["api_key_id"],
                                               user=self.context["request"].user).values(
                            "id").first()["id"]
                setattr(instance, k, v)
            instance.save()
            return instance

        except Exception:
            return None


class MMBotSerializerStatus(serializers.Serializer):
    status = serializers.CharField()

    class Meta:
        model = MarketMakerBot
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
