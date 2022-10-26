from rest_framework import serializers
from apps.geneses.models.models import *


class GenesesSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(required=True)
    api_key_id = serializers.IntegerField(required=True)
    name = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    user_order_size_bid = serializers.FloatField(required=True)
    user_order_size_ask = serializers.FloatField(required=True)
    market_value = serializers.FloatField(required=True)
    spread_distance = serializers.FloatField(required=True)

    class Meta:
        model = Geneses
        fields = (
            "id",
            "user_id",
            "api_key_id",
            "name",
            "token",
            "user_order_size_bid",
            "user_order_size_ask",
            "market_value",
            "spread_distance",
        )


class GenesesSerializerDetail(serializers.Serializer):
    class Meta:
        fields = ("id",)


class GenesesSerializerUpdate(serializers.Serializer):
    api_key_id = serializers.IntegerField(required=True)
    name = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    user_order_size_bid = serializers.FloatField(required=True)
    user_order_size_ask = serializers.FloatField(required=True)
    market_value = serializers.FloatField(required=True)
    spread_distance = serializers.FloatField(required=True)

    class Meta:
        fields = (
            "api_key_id",
            "name",
            "token",
            "user_order_size_bid",
            "user_order_size_ask",
            "market_value",
            "spread_distance",
        )

    def update(self, instance, validation_data):
        try:
            for k, v in validation_data.items():
                setattr(instance, k, v)
            instance.save()
            return instance

        except Exception:
            return None


class GenesesSerializerStatusUpdate(serializers.Serializer):
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


class GenesesSerializerStatus(serializers.ModelSerializer):
    class Meta:
        model = Geneses
        fields = ("status",)
