from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated

from apps.dashboard.db.models import *
from apps.dashboard.db.forms import *
from apps.dashboard.ex.biconomy import *
from apps.dashboard.helper.helper import *
from apps.bid.serializers import BidBotSerializer



class BidList(APIView):
    permission_classes = (IsAuthenticated,)  
    
    def get(request):
        result = BidBot.objects.filter(user__username=request.user.name).order_by("-updated_at")
        serializer = BidBotSerializer(result, many=True)
        return Response(serializer.data)


class BidAdd(APIView):
    permission_classes = (IsAuthenticated,) 

    def bidAdd(request):
        serializer = BidBotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status_code(1))


# def bidDetails
# def bidUpdate
# def bidDelete




# def bid_bot_run_status(request, pk):
#     data = BidBot.objects.filter(id=pk, user_id=request.user.id)
#     if data.status == "START":
#         return HttpResponse({"bid_bot_status": "running"})
#     else:
#         return HttpResponse({"bid_bot_status": "stoped"})


# def bid_bot_buy(request, pk):

#     bidbot = BidBot.objects.get(id=pk, user_id=request.user.id)
#     limit = bidbot.number_of_orders
#     symbol = bidbot.pair_token.pair
#     price = bidbot.trade_amount

#     order_book = bid_order_creator(limit, price, symbol)
#     order_book = order_book["order_pair"]

#     api_key = bidbot.api_key.api_key
#     api_sec = bidbot.api_key.api_secret


#     exit = []

#     for order in order_book:

#         params = {
#             "amount": float("{:.2f}".format(order["quantity"])),
#             "api_key": api_key,
#             "market": symbol,
#             "price": float("{:.6f}".format(order["price"])),
#             "side": 2,
#             "secret_key": api_sec,
#         }

#         code = create_order(params)
#         exit.append(code)
#         cancel_order_list = CancelOrderBookBID(
#             bid_bot_id=pk, cancel_order_list=code, order_status=True
#         )
#         cancel_order_list.save()
#         time.sleep(0.3)

#     # the Maximum list-to-str lenth is 505 bytes

#     return {"status": "success", "check": exit}


# def bid_bot_cancel(request, pk):

#     data = BidBot.objects.get(id=pk, user_id=request.user.id)

#     cancel_codes = (
#         CancelOrderBookBID.objects.exclude(order_status=False)
#         .filter(bid_bot_id=pk, bid_bot__user_id=request.user.id)
#         .values()
#     )

#     api_key = data.api_key.api_key
#     api_sec = data.api_key.api_secret
#     symbol = data.pair_token.pair

#     # codes = cancel_codes

#     for code in cancel_codes:

#         params = {
#             "api_key": api_key,
#             "market": symbol,
#             "order_id": code["cancel_order_list"],
#             "secret_key": api_sec,
#         }

#         try:
#             result = cancel_order(params)
#             CancelOrderBookBID.objects.filter(id=code["id"]).update(order_status=False)
#             print(result)
#         except Exception as e:
#             pass
#         time.sleep(0.3)

#     return {"status": "success"}


# # 
# def bid_bot_ctrl(request, pk):

#     try:

#         data = BidBot.objects.get(id=pk, user_id=request.user.id)
#         if data.status == "STOP":
#             BidBot.objects.filter(id=pk, user_id=request.user.id).update(status="START")
#             result = bid_bot_buy(request, pk)

#         else:
#             # Cancel all orders
#             BidBot.objects.filter(id=pk, user_id=request.user.id).update(status="STOP")
#             result = bid_bot_cancel(request, pk)

#         return redirect("dashboard:bidDetails", pk=data.id)

#     except Exception as e:
#         return JsonResponse({"status": "error", "check": str(e)})
