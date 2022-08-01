from django.shortcuts import render, redirect
from django.core.serializers import serialize
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model

from apps.dashboard.db import *
from apps.dashboard.db.models import *
from apps.dashboard.db.forms import *
from apps.dashboard.ex.biconomy import *

import json
import time

# Create your views here.
def logStore(request, ack, msg=""):
    try:
        DashboardSysLogs.objects.create(action=ack, user_id=request.user.id, data=msg)

        return {
            "status": "pass",
            "user_id": request.user.id,
            "action": ack,
            "data": msg,
        }
    except Exception as error:

        return {
            "status": "fail",
            "user_id": request.user.id,
            "action": ack,
            "data": msg,
            "exception": f"{error}",
        }


# Login
def loginc(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        #################################
        UserModel = get_user_model()
        user = request.user.is_authenticated
        if user == True:
            return redirect("dashboard:index")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard:index")
    return render(request, "registration/login.html", {"form": LoginForm})


# Logout
def logoutc(request):
    logout(request)
    return redirect("dashboard:login")


# Home dashboard
@login_required
def index(request):
    context = {"title": "Dashboard"}
    return render(request, "dashboard/pages/index.html", context)


# Blank page
@login_required
def blank(request):
    context = {}
    return render(request, "dashboard/pages/index.html", context)


# Not found error page
@login_required
def notFound(request):
    context = {}
    return render(request, "dashboard/pages/index.html", context)


# All order historic by user
@login_required
def orderHistoric(request):
    result = MarketMakerBotOrderHistory.objects.filter(bot__user_id=request.user.id)
    context = {
        "title": "Bot Order Historic",
        "historic": result,
    }
    return render(request, "dashboard/orderHistoric/orderHistoric.html", context)


# All apis by user
@login_required
def apiList(request):
    result = ApiKeys.objects.filter(user_id=request.user.id).order_by("-updated_at")
    context = {
        "title": "Api List",
        "apilist": result,
    }
    return render(request, "dashboard/api/apiList.html", context)


# Add or Update an API
@login_required
def apiAdd(request):
    if request.method == "POST":
        form = ApiForm(request.POST)
        if form.is_valid():
            apikey = form.save(commit=False)
            apikey.user_id = request.user.id
            apikey.save()
            return redirect("dashboard:apiList")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ApiForm()
    context = {
        "title": "Create new API",
        "form": form,
    }
    return render(request, "dashboard/api/apiAdd.html", context)


# Api updade
def apiUpdate(request, pk):
    instance = ApiKeys.objects.filter(id=pk).first()
    if request.method == "POST":
        form = ApiForm(request.POST or None, instance=instance)
        if form.is_valid():
            apikey = form.save(commit=False)
            apikey.user_id = request.user.id
            apikey.save()
            return redirect("dashboard:apiList")
    else:
        form = ApiForm(instance=instance)
    return render(request, "dashboard/api/apiAdd.html", {"form": form})


def apiDelete(request, pk):
    result = ApiKeys.objects.filter(id=pk)
    if request.method == "POST":
        result.delete()
        return redirect("dashboard:apiList")
    return redirect("dashboard:index")


# All bots by user
@login_required
def botList(request):
    result = MarketMakerBot.objects.filter(user=request.user.id).order_by("-updated_at")
    context = {
        "title": "Bot List",
        "botlist": result,
    }
    return render(request, "dashboard/bots/botList.html", context)


# Add or Update an Bot
@login_required
def botAdd(request):
    if request.method == "POST":
        form = BotForm(request.POST)
        if form.is_valid():
            bot = form.save(commit=False)
            bot.user_id = request.user.id
            bot.save()
            return redirect("dashboard:botList")
        else:
            print(form.errors)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = BotForm()
    context = {
        "title": "Create new bot",
        "form": form,
    }
    return render(request, "dashboard/bots/botAdd.html", context)


def botUpdate(request, pk):
    instance = MarketMakerBot.objects.filter(id=pk).first()
    if request.method == "POST":
        form = BotForm(request.POST or None, instance=instance)
        if form.is_valid():
            bot = form.save(commit=False)
            bot.user_id = request.user.id
            bot.save()
            return redirect("dashboard:botList")
    else:
        form = BotForm(instance=instance)
    return render(request, "dashboard/bot/botAdd.html", {"form": form})


def botDelete(request, pk):
    result = MarketMakerBot.objects.filter(id=pk)
    if request.method == "POST":
        result.delete()
        return redirect("dashboard:botList")
    return redirect("dashboard:index")


# Bot historic by user and bot
@login_required
def botHistory(request, pk):
    result = MarketMakerBotOrderHistory.objects.filter(bot__id=pk)
    context = {
        "title": "Bot Historic",
        "bothistoric": result,
    }
    return render(request, "dashboard/bots/botHistoric.html", context)


# All bids_bot by user
@login_required
def bidList(request):
    result = BidBot.objects.filter(user=request.user.id).order_by("-updated_at")
    context = {
        "title": "Bot List",
        "bidlist": result,
    }
    return render(request, "dashboard/bid/bidList.html", context)


# Bid bot details
@login_required
def bidDetails(request, pk):
    result = BidBot.objects.get(id=pk)
    context = {
        "title": "Bid Details",
        "biddetail": result,
    }
    return render(request, "dashboard/bid/bidDetails.html", context)


# Add or Update an Bot
@login_required
def bidAdd(request):
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            bot = form.save(commit=False)
            bot.user_id = request.user.id

            if bot.trade_amount == None:
                bot.trade_amount = 0
            
            bot.save()
            return redirect("dashboard:bidList")
        else:
            print(form.errors)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = BidForm()
    context = {
        "title": "Create new bid bot",
        "form": form,
    }
    return render(request, "dashboard/bid/bidAdd.html", context)


@login_required
def bidUpdate(request, pk):
    instance = BidBot.objects.filter(id=pk).first()
    if request.method == "POST":
        form = BotForm(request.POST or None, instance=instance)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.user_id = request.user.id
            bid.save()
            return redirect("dashboard:bidList")
    else:
        form = BotForm(instance=instance)
    return render(request, "dashboard/bid/bidAdd.html", {"form": form})


@login_required
def bidDelete(request, pk):
    result = BidBot.objects.filter(id=pk)
    if request.method == "POST":
        result.delete()
        return redirect("dashboard:bidList")
    return redirect("dashboard:index")


@login_required
def market_maker_bot_ctrl(request, pk):
    try:
        data = MarketMakerBot.objects.get(id=pk, user_id=request.user.id)
        if data.status == "STOP":
            MarketMakerBot.objects.filter(id=pk, user_id=request.user.id).update(
                status="START"
            )
        else:
            MarketMakerBot.objects.filter(id=pk, user_id=request.user.id).update(
                status="STOP"
            )

        return redirect("dashboard:botList")
        # return HttpResponse(data.status)
    except Exception as e:
        return HttpResponse({"exit": "error"})


@login_required
def market_maker_bot_run_status(request, pk):
    data = MarketMakerBot.objects.filter(id=pk, user_id=request.user.id)
    if data.status == "START":
        return HttpResponse({"bot_status": "running"})
    else:
        return HttpResponse({"bot_status": "stoped"})


def bid_bot_run_status(request, pk):
    data = BidBot.objects.filter(id=pk, user_id=request.user.id)
    if data.status == "START":
        return HttpResponse({"bid_bot_status": "running"})
    else:
        return HttpResponse({"bid_bot_status": "stoped"})


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
        time.sleep(0.3)

    return {"status": "success"}


@login_required
def bid_bot_ctrl(request, pk):

    try:

        data = BidBot.objects.get(id=pk, user_id=request.user.id)
        if data.status == "STOP":
            BidBot.objects.filter(id=pk, user_id=request.user.id).update(status="START")
            result = bid_bot_buy(request, pk)

        else:
            # Cancel all orders
            BidBot.objects.filter(id=pk, user_id=request.user.id).update(status="STOP")
            result = bid_bot_cancel(request, pk)

        return redirect("dashboard:bidDetails", pk=data.id)

    except Exception as e:
        return JsonResponse({"status": "error", "check": str(e)})
