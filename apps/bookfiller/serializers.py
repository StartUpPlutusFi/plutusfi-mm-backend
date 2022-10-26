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
        new_bookfiller = BookFiller.objects.create(
            user=self.context["request"].user,
            **validated_data
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
    user_id = serializers.IntegerField(required=True)
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
            "user_id",
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


class BookFillerSerializerResponse(serializers.ModelSerializer):
    class Meta:
        model = BookFiller
        exclude = ("status",)
