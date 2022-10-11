from django.urls import path
from apps.exchange.api.views import *

app_name = "exchange"

urlpatterns = [
    path("exchange/list", ExchangeList.as_view(), name="ExchangeList"),

    path("apikey/list", ApiKeyList.as_view(), name="ApiKeyList"),
    path("apikey/add", ApiKeyAdd.as_view(), name="ApiKeyAdd"),
    path("apikey/detail/<int:pk>", ApiKeyDetail.as_view(), name="ApiKeyDetail"),
    path("apikey/delete/<int:pk>", ApiKeyDelete.as_view(), name="ApiKeyDelete"),
    path("apikey/update/<int:pk>", ApiKeyUpdate.as_view(), name="ApiKeyUpdate"),

]

