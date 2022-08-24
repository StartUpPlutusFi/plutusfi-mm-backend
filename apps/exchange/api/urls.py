from django.urls import path
from apps.exchange.services.exchanges.api.urls import urlpatterns
from apps.exchange.services.token.api.urls import urlpatterns
from apps.exchange.services.apikeys.api.urls import urlpatterns

app_name = "exchange"
urlpatterns = [
    path("list", ExchangeList.as_view(), name="ExchangeList"),
    path("add", ExchangeAdd.as_view(), name="ExchangeAdd"),
    path("detail/<int:pk>", ExchangeDetail.as_view(), name="ExchangeDetail"),
    path("delete/<int:pk>", ExchangeDelete.as_view(), name="ExchangeDelete"),
    path("update/<int:pk>", ExchangeUpdate.as_view(), name="ExchangeUpdate"),

    path("list", TokenList.as_view(), name="TokenList"),
    path("add", TokenAdd.as_view(), name="TokenAdd"),
    path("detail/<int:pk>", TokenDetail.as_view(), name="TokenDetail"),
    path("delete/<int:pk>", TokenDelete.as_view(), name="TokenDelete"),
    path("update/<int:pk>", TokenUpdate.as_view(), name="TokenUpdate"),

    path("list", ApiKeyList.as_view(), name="ApiKeyList"),
    path("add", ApiKeyAdd.as_view(), name="ApiKeyAdd"),
    path("detail/<int:pk>", ApiKeyDetail.as_view(), name="ApiKeyDetail"),
    path("delete/<int:pk>", ApiKeyDelete.as_view(), name="ApiKeyDelete"),
    path("update/<int:pk>", ApiKeyUpdate.as_view(), name="ApiKeyUpdate"),

]
