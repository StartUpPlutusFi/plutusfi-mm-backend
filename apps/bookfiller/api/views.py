from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.dashboard.db.models import *
from apps.dashboard.helper.helper import status_code
from apps.bookfiller.serializers import *
from apps.bot.ex.biconomy import *
from apps.bookfiller.biconomy import biconomy_bookfiller


import time


class BookFillerList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookFillerSerializer

    def get_queryset(self):
        result = BookFiller.objects.filter(user=self.request.user).order_by(
            "-updated_at"
        )
        return result

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class BookFillerAdd(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookFillerSerializer

    def post(self, request, *args, **kwargs):
        insert_data = dict(request.data) | {
            "user": request.user.id,
        }

        serializer = BookFillerSerializer(data=insert_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(status_code(2))


class BookFillerDetail(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookFillerSerializer

    def get_queryset(self):
        result = BookFiller.objects.filter(
            user=self.request.user, id=self.kwargs.get("pk")
        )
        return result

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class BookFillerDelete(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        result = BookFiller.objects.filter(
            user=self.request.user, id=self.kwargs.get("pk")
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


class BookFillerUpdate(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookFillerSerializerUpdate

    def get_queryset(self):
        result = BookFiller.objects.filter(
            user=self.request.user, id=self.kwargs.get("pk")
        ).first()
        return result

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.update(self.get_queryset(), validation_data=serializer.data)
        return Response(BookFillerSerializer(data).data)


class BookFillerStatus(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookFillerSerializerStatus

    def get_queryset(self):
        data = BookFiller.objects.filter(
            id=self.kwargs.get("pk"), user=self.request.user
        )
        return data

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


def BookFiller_bot_buy(request, pk):
    bookfiller = BookFiller.objects.get(id=pk, user_id=request.user.id)
    limit = bookfiller.number_of_orders
    symbol = bookfiller.pair_token.pair
    price = bookfiller.budget

    order_book = bid_order_creator(limit, price, symbol)
    order_book = order_book["order_pair"]

    api_key = bookfiller.api_key.api_key
    api_sec = bookfiller.api_key.api_secret

    exit_code = []

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
        exit_code.append(code)
        cancel_order_list = CancelOrderBookBookFiller(
            BookFiller_bot_id=pk, cancel_order_list=code, order_status=True
        )
        cancel_order_list.save()
        time.sleep(0.3)

    # the Maximum list-to-str length is 505 bytes

    return {"status": "success", "check": exit}


def BookFiller_bot_cancel(request, pk):
    data = BookFiller.objects.get(id=pk, user_id=request.user.id)

    cancel_codes = (
        CancelOrderBookBookFiller.objects.exclude(order_status=False)
        .filter(BookFiller_bot_id=pk, BookFiller_bot__user_id=request.user.id)
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
            CancelOrderBookBookFiller.objects.filter(id=code["id"]).update(
                order_status=False
            )
            # print(result)
        except Exception as e:
            pass
        time.sleep(0.25)

    return {"status": "success"}


class BookFillerCtrl(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BookFillerSerializerStatusUpdate

    def get_queryset(self):
        result = BookFiller.objects.filter(
            user=self.request.user, id=self.kwargs.get("pk")
        ).first()
        return result

    def get(self, request, *args, **kwargs):
        if True:
            data = self.get_queryset()
            bot_ex = data.api_key.exchange.name
            all_ex = Exchange.objects.all().values('name')

            if data.status == "STOP":

                for ex in all_ex:
                
                    if ex['name'] == bot_ex:
                        # op_result = biconomy_bookfiller.biconomy_init_bookbot(data)
                        return Response("pass")
                    else:
                        pass
                
                # EndFor

                BookFiller.objects.filter(
                    id=self.kwargs.get("pk"), user=request.user
                ).update(status="START")

            else:
                
                # Cancel all orders
                # biconomy_bookfiller.biconomy_cancel_all_orders(data.id)

                BookFiller.objects.filter(
                    id=self.kwargs.get("pk"), user=request.user
                ).update(status="STOP")


            return Response("pass two")
            
        # except Exception as e:
        #     return Response({"status": "error", "check": str(e)})
