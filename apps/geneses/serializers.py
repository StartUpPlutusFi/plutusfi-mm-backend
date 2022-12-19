from rest_framework import serializers
from apps.geneses.models.models import *


class GenesesSerializer(serializers.ModelSerializer):
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
            "api_key_id",
            "name",
            "token",
            "user_order_size_bid",
            "user_order_size_ask",
            "market_value",
            "spread_distance",
        )

    def create(self, validated_data):
        validated_data = validated_data | {
            "api_key_id": ApiKeys.objects.filter(
                id=validated_data["api_key_id"], user=self.context["request"].user
            )
            .values("id")
            .first()["id"],
        }
        new_geneses = Geneses.objects.create(
            user=self.context["request"].user, **validated_data
        )
        new_geneses.save()
        return new_geneses


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


class GenesesSerializerStatusUpdate(serializers.Serializer):
    status = serializers.CharField()

    class Meta:
        model = Geneses
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


class GenesesSerializerResponse(serializers.ModelSerializer):
    class Meta:
        model = Geneses
        fields = '__all__'
