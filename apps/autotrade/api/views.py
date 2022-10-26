# # Create your views here.

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view

from apps.autotrade.serializers import *
from apps.autotrade.models.models import *
from apps.exchange.helper.helper import status_code


class MMbotList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MMBotSerializer

    def get_queryset(self):
        result = MarketMakerBot.objects.filter(user=self.request.user).order_by(
            "-created_at"
        )
        return result

    def get(self, request, *args, **kwargs):
        # logging.info(self.get_queryset().values())
        return self.list(request, *args, **kwargs)


class MMbotAdd(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MMBotSerializerAdd

    def post(self, request, *args, **kwargs):

        try:
            res = dict(request.data)
            insert_data = res | {
                "user_id": request.user.id,
                "api_key_id": ApiKeys.objects.filter(
                    id=res["api_key_id"], user_id=request.user.id
                )
                .values("id")
                .first()["id"],
            }

            serializer = MMBotSerializerAdd(data=insert_data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(status_code(5, f"Data is invalid {serializer}"))

        except Exception as err:
            return Response(
                {
                    "status": "error",
                    "msg": "invalid data or unauthorized api_key_id",
                    "code": str(err),
                }
            )


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
            if self.destroy(request, *args, **kwargs):
                return Response({"status": "done"})
            else:
                return Response(
                    {"status": "data not found"}, status=status.HTTP_404_NOT_FOUND
                )

        except Exception as err:
            return Response(
                {"status": "data not found"}, status=status.HTTP_404_NOT_FOUND
            )


class MMbotUpdate(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MMBotSerializerUpdate
    http_method_names = ("put",)

    def get_queryset(self):
        result = MarketMakerBot.objects.filter(
            user=self.request.user, id=self.kwargs.get("pk")
        ).first()
        return result

    def put(self, request, *args, **kwargs):
        try:
            res = dict(request.data)
            insert_data = res | {
                "user_id": request.user.id,
                "api_key_id": ApiKeys.objects.filter(
                    id=res["api_key_id"], user_id=request.user.id
                )
                .values("id")
                .first()["id"],
            }
            serializer = self.serializer_class(data=insert_data)
            serializer.is_valid(raise_exception=True)
            data = serializer.update(
                self.get_queryset(), validation_data=serializer.data
            )
            return Response(MMBotSerializer(data).data)

        except Exception as err:

            return Response(
                {
                    "status": "error",
                    "msg": "invalid data or unauthorized api_key_id",
                    "code": str(err),
                }
            )


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
    http_method_names = ("get",)

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
