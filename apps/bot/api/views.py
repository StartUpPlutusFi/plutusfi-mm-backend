# Create your views here.
from random import randint
from unittest import result
from rest_framework.response import Response
from rest_framework import generics

from rest_framework.permissions import IsAuthenticated

from apps.dashboard.db.models import *
from apps.dashboard.db.forms import *
from apps.dashboard.helper.helper import *
from apps.bot.serializers import *

from apps.autotrade.api.views import *


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

            print(insert_data)
            serializer = MMBotSerializer(data=insert_data)

        except Exception as e:

            return Response(str(e) )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(status_code(5, f"Data is invalid { serializer }"))


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


class BotCtrl(generics.UpdateAPIView):
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
            
            apikey = data.api_key.api_key
            apisec = data.api_key.api_secret


            user_side_choice = randint(1,2)
            user_max_order_value = data.trade_amount
            token = data.pair_token.pair

            user_ref_price = 0
            exit = check_ref_price(token)

            # check_ref_price(token)

            result = random_bid_ask_order(user_ref_price, user_side_choice, user_max_order_value, apikey, apisec, token)

            return Response({
                "reference_price": exit[0],
                "user_ref_price": user_ref_price, 
                "user_side_choice": user_side_choice, 
                "user_max_order_value": user_max_order_value, 
                "token": token, 
                "side": data.side, 
                "status": data.status,
                "random_bid_ask_order_result": result,
            })

            # return result

        except Exception as e:
            return Response({"status": "error", "check": str(e)})
