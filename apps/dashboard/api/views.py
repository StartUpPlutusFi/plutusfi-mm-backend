from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


from apps.dashboard.db import *
from apps.dashboard.db.models import *
from apps.dashboard.db.forms import *
from apps.dashboard.ex.biconomy import *

from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class LogStore(APIView):
    permission_classes = (IsAuthenticated,)

    def get(request):
        try:
            DashboardSysLogs.objects.create(
                action=request.body.ack, user_id=request.user.id, data=request.body.msg
            )
            return Response(
                {
                    "status": "pass",
                    "user_id": request.user.id,
                    "action": request.body.ack,
                    "data": request.body.msg,
                }
            )
        except Exception as e:

            return Response(
                {
                    "status": "pass",
                    "user_id": request.user.id,
                    "action": request.body.ack,
                    "data": request.body.msg,
                }
            )


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
