# Create your views here.
from requests import request
from rest_framework.response import Response
from rest_framework import generics

from rest_framework.permissions import IsAuthenticated

from apps.dashboard.db.models import *
from apps.dashboard.db.forms import *
from apps.dashboard.helper.helper import *
from apps.bot.serializers import *


class MMbotList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MMBotSerializer

    def get_queryset(self):
        result = MarketMakerBot.objects.filter(user=self.request.user)
        return result

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class MMbotAdd(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = MMBotSerializer(data=request.data)
        data = dict(data.initial_data) | {"user": request.user.id}
        serializer = MMBotSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status_code(2))


class MMbotDetail(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MMBotSerializer

    def get_queryset(self):
        result = MarketMakerBot.objects.filter(
            user=self.request.user, id=self.kwargs.get("pk")
        )
        return result

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class MMbotDelete(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        result = MarketMakerBot.objects.filter(
            id=self.kwargs.get("pk"), user=self.request.user
        )
        return result

    def delete(self, request, *args, **kwargs):
        try:
            return self.destroy(request, *args, **kwargs)
        except Exception as e:
            return Response(
                status_code(
                    5,
                    "Cannot delete a parent row, check foreign key constraint or if the object exist",
                )
            )


class MMbotUpdate(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MMBotSerializerUpdate

    def get_queryset(self):
        result = MarketMakerBot.objects.filter(
            id=self.kwargs.get("pk"), user=self.request.user
        ).first()
        return result

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.update(self.get_queryset(), validation_data=serializer.data)
        return Response(MMBotSerializer(data).data)
