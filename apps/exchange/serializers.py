from rest_framework import serializers

from apps.exchange.helper.crypto_utils import EncryptationTool
from apps.exchange.models.models import *


# ------------------------------------------------------------------------------------ #
# ApiKey Serializer
class ApiKeySerializer(serializers.ModelSerializer):
    api_key = serializers.CharField(required=True, allow_null=False)
    api_secret = serializers.CharField(required=True, allow_null=False)
    description = serializers.CharField(required=True, allow_null=False)
    default = serializers.BooleanField(required=True, allow_null=False)

    class Meta:
        model = ApiKeys
        fields = (
            "api_key",
            "api_secret",
            "description",
            "default",
            "exchange",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        api_key_encrypted = EncryptationTool.encrypt(validated_data.get("api_key").encode())
        api_secret_encrypted = EncryptationTool.encrypt(validated_data.get("api_secret").encode())
        validated_data.pop("api_key")
        validated_data.pop("api_secret")

        new_api_key = ApiKeys.objects.create(
            user=user,
            api_key=api_key_encrypted,
            api_secret=api_secret_encrypted,
            **validated_data
        )

        new_api_key.save()

        return new_api_key


class ApiKeySerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = ApiKeys
        fields = (
            "id",
            "description",
            "default",
            "exchange",
        )


class ApiKeySerializerUpdate(serializers.Serializer):
    description = serializers.CharField(required=False)
    default = serializers.BooleanField(required=False)

    class Meta:
        fields = (
            "description",
            "default",
        )

    def update(self, instance, validation_data):
        try:
            for k, v in validation_data.items():
                setattr(instance, k, v)
            instance.save()
            return instance

        except Exception:
            return None


# ------------------------------------------------------------------------------------ #
# @ Exchange Serializer


class ExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields = "__all__"


class ExchangeSerializerDetail(serializers.Serializer):
    class Meta:
        fields = ("id",)


class ExchangeSerializerUpdate(serializers.Serializer):
    name = serializers.CharField(required=False)

    class Meta:
        fields = ("name",)

    def update(self, instance, validation_data):
        try:
            for k, v in validation_data.items():
                setattr(instance, k, v)
            instance.save()
            return instance

        except Exception:
            return None
