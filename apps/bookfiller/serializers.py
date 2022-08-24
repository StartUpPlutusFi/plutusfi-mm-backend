from rest_framework import serializers
from apps.bookfiller.db.models import *


class BookFillerSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    side = serializers.CharField(required=True)
    order_size = serializers.IntegerField(required=True)
    number_of_orders = serializers.IntegerField(required=True)
    budget = serializers.FloatField(required=True)
    user_ref_price = serializers.FloatField(required=True)
    status = serializers.CharField(required=True)

    class Meta:
        model = BookFiller
        fields = (
            "id",
            "name",
            "side",
            "user",
            "api_key",
            "pair_token",
            "order_size",
            "number_of_orders",
            "budget",
            "user_ref_price",
            "status",
        )


class BookFillerSerializerStatus(serializers.ModelSerializer):
    class Meta:
        model = BookFiller
        fields = ("status",)


class BookFillerSerializerDetail(serializers.Serializer):
    class Meta:
        fields = ("id",)


class BookFillerSerializerUpdate(serializers.Serializer):
    name = serializers.CharField(required=False)
    order_size = serializers.IntegerField(required=False)
    number_of_orders = serializers.IntegerField(required=False)
    budget = serializers.FloatField(required=False)
    user_ref_price = serializers.FloatField(required=False)
    api_key = serializers.IntegerField(required=False)

    class Meta:
        fields = (
            "name",
            "order_size",
            "number_of_orders",
            "budget",
            "user_ref_price",
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


class BookFillerSerializerStatusUpdate(serializers.Serializer):
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
