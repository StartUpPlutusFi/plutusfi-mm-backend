from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import generics

from rest_framework.permissions import IsAuthenticated

from apps.dashboard.db.models import *
from apps.dashboard.db.forms import *
from apps.dashboard.ex.biconomy import *
from apps.dashboard.helper.helper import *
from apps.bid.serializers import *

import time


class BidList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BidBotSerializer

    def get_queryset(self):
        result = BidBot.objects.filter(user=self.request.user).order_by("-updated_at")
        return result

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class BidAdd(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = BidBotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status_code(2))


class BidDetail(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BidBotSerializer

    def get_queryset(self):
        result = BidBot.objects.filter(user=self.request.user, id=self.kwargs.get("pk"))
        return result

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class BidDelete(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        result = BidBot.objects.filter(user=self.request.user, id=self.kwargs.get("pk"))
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


class BidUpdate(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BidBotSerializerUpdate

    def get_queryset(self):
        result = BidBot.objects.filter(
            user=self.request.user, id=self.kwargs.get("pk")
        ).first()
        return result

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.update(self.get_queryset(), validation_data=serializer.data)
        return Response(BidBotSerializer(data).data)


class BidStatus(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BidBotSerializerStatus

    def get_queryset(self):
        data = BidBot.objects.filter(id=self.kwargs.get("pk"), user=self.request.user)
        return data

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


def bid_bot_buy(request, pk):

    bidbot = BidBot.objects.get(id=pk, user_id=request.user.id)
    limit = bidbot.number_of_orders
    symbol = bidbot.pair_token.pair
    price = bidbot.trade_amount

    order_book = bid_order_creator(limit, price, symbol)
    order_book = order_book["order_pair"]

    api_key = bidbot.api_key.api_key
    api_sec = bidbot.api_key.api_secret

    exit = []

    for order in order_book:

        params = {
            "amount": float("{:.2f}".format(order["quantity"])),
            "api_key": api_key,
            "market": symbol,
            "price": float("{:.6f}".format(order["price"])),
            "side": 2,
            "secret_key": api_sec,
        }

        code = create_order(params)
        exit.append(code)
        cancel_order_list = CancelOrderBookBID(
            bid_bot_id=pk, cancel_order_list=code, order_status=True
        )
        cancel_order_list.save()
        time.sleep(0.3)

    # the Maximum list-to-str lenth is 505 bytes

    return {"status": "success", "check": exit}


def bid_bot_cancel(request, pk):

    data = BidBot.objects.get(id=pk, user_id=request.user.id)

    cancel_codes = (
        CancelOrderBookBID.objects.exclude(order_status=False)
        .filter(bid_bot_id=pk, bid_bot__user_id=request.user.id)
        .values()
    )

    api_key = data.api_key.api_key
    api_sec = data.api_key.api_secret
    symbol = data.pair_token.pair

    # codes = cancel_codes

    for code in cancel_codes:

        params = {
            "api_key": api_key,
            "market": symbol,
            "order_id": code["cancel_order_list"],
            "secret_key": api_sec,
        }

        try:
            result = cancel_order(params)
            CancelOrderBookBID.objects.filter(id=code["id"]).update(order_status=False)
            print(result)
        except Exception as e:
            pass
        time.sleep(0.25)

    return {"status": "success"}


class BidCtrl(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BidBotSerializerStatusUpdate

    def get_queryset(self):
        result = BidBot.objects.filter(
            user=self.request.user, id=self.kwargs.get("pk")
        ).first()
        return result

    def get(self, request, *args, **kwargs):
        try:
            data = self.get_queryset()
            if data.status == "STOP":
                result = bid_bot_buy(request, self.kwargs.get("pk"))
                BidBot.objects.filter(
                    id=self.kwargs.get("pk"), user_id=request.user
                ).update(status="START")

            else:
                # Cancel all orders
                result = bid_bot_cancel(request, self.kwargs.get("pk"))
                BidBot.objects.filter(
                    id=self.kwargs.get("pk"), user_id=request.user
                ).update(status="STOP")

            return Response(result)
        except Exception as e:
            return JsonResponse({"status": "error", "check": str(e)})
