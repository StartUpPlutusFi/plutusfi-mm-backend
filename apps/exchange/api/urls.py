from django.urls import path
from apps.exchange.api.views import *

app_name = "exchange"

urlpatterns = [
    path("exchange/list", ExchangeList.as_view(), name="ExchangeList"),
    path("exchange/add", ExchangeAdd.as_view(), name="ExchangeAdd"),
    path("exchange/detail/<int:pk>", ExchangeDetail.as_view(), name="ExchangeDetail"),
    path("exchange/delete/<int:pk>", ExchangeDelete.as_view(), name="ExchangeDelete"),
    path("exchange/update/<int:pk>", ExchangeUpdate.as_view(), name="ExchangeUpdate"),

    path("apikey/list", ApiKeyList.as_view(), name="ApiKeyList"),
    path("apikey/add", ApiKeyAdd.as_view(), name="ApiKeyAdd"),
    path("apikey/detail/<int:pk>", ApiKeyDetail.as_view(), name="ApiKeyDetail"),
    path("apikey/delete/<int:pk>", ApiKeyDelete.as_view(), name="ApiKeyDelete"),
    path("apikey/update/<int:pk>", ApiKeyUpdate.as_view(), name="ApiKeyUpdate"),

]

