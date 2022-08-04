from numpy import require
from rest_framework import serializers
from apps.dashboard.db.models import *


class BidBotSerializer(serializers.ModelSerializer):

    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    order_size = serializers.IntegerField(required=True)
    number_of_orders = serializers.IntegerField(required=True)
    budget = serializers.FloatField(required=True)
    trade_amount = serializers.FloatField(required=True)
    status = serializers.CharField(required=True)

    class Meta:
        model = BidBot
        fields = (
            "id", "name", "description", "user", "api_key", 
            "pair_token", "order_size", "number_of_orders", 
            "budget", "trade_amount", "status",
        )



class BidBotSerializerStatus(serializers.ModelSerializer):
    class Meta:
        model = BidBot
        fields = ("status",)


class BidBotSerializerDetail(serializers.Serializer):
    class Meta:
        fields = ("id",)


class BidBotSerializerUpdate(serializers.Serializer):

    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    order_size = serializers.IntegerField(required=False)
    number_of_orders = serializers.IntegerField(required=False)
    budget = serializers.FloatField(required=False)
    trade_amount = serializers.FloatField(required=False)
    api_key = serializers.IntegerField(required=False)

    class Meta:
        fields = (
            "name",
            "description",
            "order_size",
            "number_of_orders",
            "budget",
            "trade_amount",
            "api_key",
        )

    def update(self, instance, validation_data):
        try:
            for k, v in validation_data.items():
                setattr(instance, k, v)
            instance.save()
            return instance
        except Exception as e:

            return None


class BidBotSerializerStatusUpdate(serializers.Serializer):

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
