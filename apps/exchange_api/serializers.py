from numpy import require
from rest_framework import serializers
from apps.dashboard.db.models import *

class ApiKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiKeys
        fields = '__all__'


class ApiKeySerializerDetail(serializers.Serializer):
    class Meta:
        fields = ('id',)

class ApiKeySerializerUpdate(serializers.Serializer):
    
    name = serializers.CharField(required=False)
    api_key = serializers.CharField(required=False)    
    api_secret = serializers.CharField(required=False) 
    description = serializers.CharField(required=False)
    default = serializers.BooleanField(required=False)    
    class Meta:
        fields = ('name','api_key' ,'api_secret' ,'description' ,'default', )
 

    def update(self, instance, validation_data):
        for k, v in validation_data.items():
            setattr(instance, k, v)
        instance.save()
        return instance

