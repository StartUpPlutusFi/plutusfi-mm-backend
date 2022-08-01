from rest_framework import serializers
from apps.dashboard.db.models import *

class BidBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = BidBot
        fields = '__all__'
