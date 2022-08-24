# Create your views here.
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.autotrade.serializers import *
from apps.autotrade.db.models import *


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
    serializer_class = MMBotSerializer

    def post(self, request, *args, **kwargs):

        try:
            insert_data = dict(request.data) | {
                "user": request.user.id,
                "api_key": ApiKeys.objects.filter(
                    user=request.user, id=request.data["api_key"]
                )
                .values("id")
                .first()["id"],
                "pair_token": BotConfigPairtokens.objects.filter(
                    id=request.data["pair_token"]
                )
                .values("id")
                .first()["id"],
            }

            # print(insert_data)
            serializer = MMBotSerializer(data=insert_data)

        except Exception as e:

            return Response(str(e))

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(status_code(5, f"Data is invalid {serializer}"))


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
            user=self.request.user, id=self.kwargs.get("pk")
        ).first()
        return result

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.update(self.get_queryset(), validation_data=serializer.data)
        return Response(MMBotSerializer(data).data)


class AutoTradeStatus(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MMBotSerializerStatus

    def get_queryset(self):
        data = MarketMakerBot.objects.filter(
            id=self.kwargs.get("pk"), user=self.request.user
        ).values("status")
        return data

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class AutoTradeBotCtrl(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MMBotSerializerUpdate

    def get_queryset(self):
        try:
            result = MarketMakerBot.objects.filter(
                user=self.request.user, id=self.kwargs.get("pk")
            ).first()
            return result
        except Exception:
            return {}

    def get(self, request, *args, **kwargs):
        try:

            data = self.get_queryset()

            if data.status == "STOP":
                MarketMakerBot.objects.filter(
                    user=self.request.user, id=self.kwargs.get("pk")
                ).update(status="START")
                exit_code = "START"
            else:
                MarketMakerBot.objects.filter(
                    user=self.request.user, id=self.kwargs.get("pk")
                ).update(status="STOP")
                exit_code = "STOP"

            return Response(
                {
                    "status": "success",
                    "auto_trade_bot_status": exit_code,
                }
            )

        except Exception as e:
            return Response(
                {
                    "status": "error",
                    "code": str(e),
                }
            )
