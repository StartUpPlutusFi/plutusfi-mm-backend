from django.urls import path
from .views import *

app_name = "MMbot"
urlpatterns = [
    path("list", MMbotList.as_view(), name="MMbotList"),
    path("add", MMbotAdd.as_view(), name="MMbotAdd"),
    path("detail/<int:pk>", MMbotDetail.as_view(), name="MMbotDetail"),
    path("delete/<int:pk>", MMbotDelete.as_view(), name="MMbotDelete"),
    path("update/<int:pk>", MMbotUpdate.as_view(), name="MMbotUpdate"),

    path("status/<int:pk>", AutoTradeStatus.as_view(), name="AutoTradeStatus"),
    path("ctrl/<int:pk>", AutoTradeStatus.as_view(), name="MMbotCtrl"),
]
