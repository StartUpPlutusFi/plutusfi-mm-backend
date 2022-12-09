from rest_framework import serializers

from apps.bookfiller.models.models import *


class BookFillerSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    side = serializers.CharField(required=True)
    order_size = serializers.IntegerField(required=True)
    api_key_id = serializers.IntegerField(required=True)
    pair_token = serializers.CharField(required=True)
    number_of_orders = serializers.IntegerField(required=True)
    budget = serializers.FloatField(required=True)
    user_ref_price = serializers.FloatField(required=True)

    class Meta:
        model = BookFiller
        fields = (
            "id",
            "name",
            "side",
            "api_key_id",
            "pair_token",
            "order_size",
            "number_of_orders",
            "budget",
            "user_ref_price",
        )

    def create(self, validated_data):
        validated_data = validated_data | {
            "api_key_id": ApiKeys.objects.filter(
                id=validated_data["api_key_id"], user=self.context["request"].user
            )
            .values("id")
            .first()["id"],
        }
        new_bookfiller = BookFiller.objects.create(
            user=self.context["request"].user, **validated_data
        )
        new_bookfiller.save()
        return new_bookfiller


class BookFillerSerializerStatus(serializers.ModelSerializer):
    class Meta:
        model = BookFiller
        fields = ("status",)


class BookFillerSerializerDetail(serializers.Serializer):
    class Meta:
        fields = ("id",)


class BookFillerSerializerUpdate(serializers.Serializer):
    name = serializers.CharField(required=True)
    side = serializers.CharField(required=True)
    order_size = serializers.IntegerField(required=True)
    api_key_id = serializers.IntegerField(required=True)
    pair_token = serializers.CharField(required=True)
    number_of_orders = serializers.IntegerField(required=True)
    budget = serializers.FloatField(required=True)
    user_ref_price = serializers.FloatField(required=True)

    class Meta:
        fields = (
            "name",
            "side",
            "api_key_id",
            "pair_token",
            "order_size",
            "number_of_orders",
            "budget",
            "user_ref_price",
        )

    def update(self, instance, validation_data):
        try:
            for k, v in validation_data.items():
                if k == "api_key_id":
                    v = \
                    ApiKeys.objects.filter(id=validation_data["api_key_id"], user=self.context["request"].user).values(
                        "id").first()["id"]
                setattr(instance, k, v)
            instance.save()
            return instance

        except Exception:
            return None


class BookFillerSerializerStatusUpdate(serializers.Serializer):
    status = serializers.CharField()

    class Meta:
        model = BookFiller
        fields = ("status",)

    def update(self, instance, validation_data):
        try:
            for k, v in validation_data.items():
                setattr(instance, k, v)
            instance.save()
            return instance

        except Exception:
            return None


class BookFillerSerializerResponse(serializers.ModelSerializer):
    class Meta:
        model = BookFiller
        exclude = ("status",)


class BookFillerCancelCodeSerializerResponse(serializers.ModelSerializer):
    class Meta:
        many = True
        model = CancelOrderBookBot
        fields = (
            "id",
            "bot_id",
            "cancel_order_id",
            "order_status",
            "created_at",
            "updated_at",
        )

    def list_all(self, data):
        return data.values()

