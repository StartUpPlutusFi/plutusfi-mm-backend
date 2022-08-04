from numpy import require
from rest_framework import serializers
from apps import exchange
from apps.dashboard.db.models import *


class ApiKeySerializer(serializers.ModelSerializer):

    api_key = serializers.CharField(required=True, allow_null=False)
    api_secret = serializers.CharField(required=True, allow_null=False)
    description = serializers.CharField(required=True, allow_null=False)
    default = serializers.BooleanField(required=True, allow_null=False)

    class Meta:
        model = ApiKeys
        fields = ("api_key", "api_secret", "description", "default", "exchange", "user", )

class ApiKeySerializerDetail(serializers.Serializer):
    class Meta:
        fields = ("id",)


class ApiKeySerializerUpdate(serializers.Serializer):

    api_key = serializers.CharField(required=False)
    api_secret = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    default = serializers.BooleanField(required=False)
    exchange = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        fields = (
            "name",
            "api_key",
            "api_secret",
            "description",
            "default",
            "exchange",
        )

    def update(self, instance, validation_data):
        try:
            for k, v in validation_data.items():
                setattr(instance, k, v)
            instance.save()
            return instance

        except Exception:
            return None
