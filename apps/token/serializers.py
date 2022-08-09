from numpy import require
from rest_framework import serializers
from apps.dashboard.db.models import *


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotConfigPairtokens
        fields = "__all__"


class TokenSerializerDetail(serializers.Serializer):
    class Meta:
        fields = ("id",)


class TokenSerializerUpdate(serializers.Serializer):

    pair = serializers.CharField(required=False)

    class Meta:
        fields = ("pair",)

    def update(self, instance, validation_data):
        try:
            for k, v in validation_data.items():
                setattr(instance, k, v)
            instance.save()
            return instance

        except Exception:
            return None
