from django.urls import path
from . import views

app_name = "dashboard"


api = [
    path("api/add", views.apiList, name="apiList"),
    path("api/list", views.apiAdd, name="apiAdd"),
    path("api/update/<int:pk>/", views.apiUpdate, name="apiUpdate"),
    path("api/delete/<int:pk>/", views.apiDelete, name="apiDelete"),
]

bid_bot = [
    path("bid/add", views.bidList, name="bidList"),
    path("bid/list", views.bidAdd, name="bidAdd"),
    path("bid/detail/<int:pk>/", views.bidDetails, name="bidDetails"),
    path("bid/update/<int:pk>/", views.bidUpdate, name="bidUpdate"),
    path("bid/delete/<int:pk>/", views.bidDelete, name="bidDelete"),
    path("bid/ctrl/<int:pk>/", views.bid_bot_ctrl, name="bidCtrl"),
    path("bid/status/<int:pk>/", views.bid_bot_run_status, name="bidStatus"),
    path("bid/buy/<int:pk>/", views.bid_bot_buy, name="bidBuy"),
    path("bid/cancel/<int:pk>/", views.bid_bot_cancel, name="bidCancel"),
]

hisotric = [
    path("order/historic", views.orderHistoric, name="orderHistoric"),
]

bots = [
    path("bot/list", views.botList, name="botList"),
    path("bot/add", views.botAdd, name="botAdd"),
    path("bot/update/<int:pk>/", views.botUpdate, name="botUpdate"),
    path("bot/delete/<int:pk>/", views.botDelete, name="botDelete"),
    path("bot/historic/<int:pk>/", views.botHistory, name="botHistory"),
    path("bot/ctrl/<int:pk>/", views.market_maker_bot_ctrl, name="botCtrl"),
    path("bot/status/<int:pk>/", views.market_maker_bot_run_status, name="botStatus"),
]

urlpatterns = (
    [
        path("", views.index, name="index"),
        path("blank/", views.blank, name="blank"),
        path("404/", views.notFound, name="notFound"),
        path("accounts/login/", views.loginc, name="login"),
        path("accounts/logout/", views.logoutc, name="logout"),
    ]
    + bots
    + hisotric
    + api
    + bid_bot
)
