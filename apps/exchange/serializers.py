from numpy import require
from rest_framework import serializers
from apps.dashboard.db.models import *

class ExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields = '__all__'


class ExchangeSerializerDetail(serializers.Serializer):
    class Meta:
        fields = ('id',)

class ExchangeSerializerUpdate(serializers.Serializer):
    
    name = serializers.CharField(required=False)

    class Meta:
        fields = ('name',)

    def update(self, instance, validation_data):
        for k, v in validation_data.items():
            setattr(instance, k, v)
        instance.save()
        return instance

