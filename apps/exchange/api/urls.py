from django.urls import path
from .views import *

app_name = "exchange"
urlpatterns = [
    path("list", ExchangeList.as_view(), name="exListTokens"),
    path("add", ExchangeAdd.as_view(), name="ExchangeAdd"),
    path("detail/<int:pk>", ExchangeDetail.as_view(), name="ExchangeDetail"),
    path("delete/<int:pk>", ExchangeDelete.as_view(), name="ExchangeDelete"),
    path("update/<int:pk>", ExchangeUpdate.as_view(), name="ExchangeUpdate"),


    
]
