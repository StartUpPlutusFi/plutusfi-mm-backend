# Create your views here.
from numpy import insert
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

        try:
            insert_data = dict(request.data) | {
                "user": request.user.id,
                "api_key": ApiKeys.objects.filter(user=request.user, id=request.data['api_key']).values('id').first()['id'],
                "pair_token": BotConfigPairtokens.objects.filter(id=request.data['pair_token']).values('id').first()['id'],
            }

            print(insert_data)
            serializer = MarketMakerBot(data=insert_data)
        
        except:

            return Response(status_code(5, "Unauthorized key access"))
        
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
        data = MarketMakerBot.objects.filter(id=self.kwargs.get("pk"), user=self.request.user).values('status')
        return data

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


# class BotCtrl(generics.UpdateAPIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = MMBotSerializerStatusUpdate

#     def get_queryset(self):
#         result = BidBot.objects.filter(
#             user=self.request.user, id=self.kwargs.get("pk")
#         ).first()
#         return result

#     def get(self, request, *args, **kwargs):
#         try:
#             data = self.get_queryset()
#             if data.status == "STOP":
#                 result = bid_bot_buy(request, self.kwargs.get("pk"))
#                 BidBot.objects.filter(
#                     id=self.kwargs.get("pk"), user=request.user
#                 ).update(status="START")

#             else:
#                 # Cancel all orders
#                 result = bid_bot_cancel(request, self.kwargs.get("pk"))
#                 BidBot.objects.filter(
#                     id=self.kwargs.get("pk"), user=request.user
#                 ).update(status="STOP")

#             return Response(result)
#         except Exception as e:
#             return JsonResponse({"status": "error", "check": str(e)})