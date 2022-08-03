from numpy import require
from rest_framework import serializers
from apps.dashboard.db.models import *


class BidBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = BidBot
        fields = "__all__"


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
    api_key_id = serializers.IntegerField(required=False)

    class Meta:
        fields = (
            "name",
            "description",
            "order_size",
            "number_of_orders",
            "budget",
            "trade_amount",
            "api_key_id",
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

    status = serializers.BooleanField()

    class Meta:
        fields = ("status",)

    def update(self, instance, validation_data):
        for k, v in validation_data.items():
            setattr(instance, k, v)
        instance.save()
        return instance
