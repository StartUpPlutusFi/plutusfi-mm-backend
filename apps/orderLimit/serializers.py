from rest_framework import serializers

from apps.exchange.models.models import *
from apps.orderLimit.models.models import OrderLimit


class OrderLimitSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    api_key_id = serializers.IntegerField(required=True)
    side = serializers.CharField(required=True)
    pair_token = serializers.CharField(required=True)
    quantity = serializers.FloatField(required=True)
    price = serializers.FloatField(required=True)

    class Meta:
        model = OrderLimit
        fields = (
            "name",
            "api_key_id",
            "side",
            "pair_token",
            "quantity",
            "price",
        )

    def create(self, validated_data):
        validated_data = validated_data | {
            "api_key_id": ApiKeys.objects.filter(
                id=validated_data["api_key_id"], user=self.context["request"].user
            )
            .values("id")
            .first()["id"],
        }
        new_bookfiller = OrderLimit.objects.create(
            user=self.context["request"].user, **validated_data
        )
        new_bookfiller.save()
        return new_bookfiller


class OrderLimitSerializerStatus(serializers.ModelSerializer):
    class Meta:
        model = OrderLimit
        fields = ("status",)


class OrderLimitSerializerDetail(serializers.Serializer):
    class Meta:
        fields = ("id",)


class OrderLimitSerializerUpdate(serializers.Serializer):
    name = serializers.CharField(required=True)
    api_key_id = serializers.IntegerField(required=True)
    side = serializers.IntegerField(required=True)
    pair_token = serializers.CharField(required=True)
    quantity = serializers.FloatField(required=True)
    price = serializers.FloatField(required=True)

    class Meta:
        model = OrderLimit
        fields = (
            "name",
            "api_key_id",
            "side",
            "pair_token",
            "quantity",
            "price",
        )

    def update(self, instance, validation_data):
        try:
            for k, v in validation_data.items():
                if k == "api_key_id":
                    v = (
                        ApiKeys.objects.filter(
                            id=validation_data["api_key_id"],
                            user=self.context["request"].user,
                        )
                        .values("id")
                        .first()["id"]
                    )
                setattr(instance, k, v)
            instance.save()
            return instance

        except Exception:
            return None


class OrderLimitSerializerStatusUpdate(serializers.Serializer):
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


class OrderLimitSerializerResponse(serializers.ModelSerializer):
    class Meta:
        model = OrderLimit
        exclude = ("status",)
