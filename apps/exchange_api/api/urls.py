from django.urls import path
from .views import *

app_name = "apikey"
urlpatterns = [
    path("list", ApiKeyList.as_view(), name="ApiKeyList"),
    path("add", ApiKeyAdd.as_view(), name="ApiKeyAdd"),
    path("detail/<int:pk>", ApiKeyDetail.as_view(), name="ApiKeyDetail"),
    path("delete/<int:pk>", ApiKeyDelete.as_view(), name="ApiKeyDelete"),
    path("update/<int:pk>", ApiKeyUpdate.as_view(), name="ApiKeyUpdate"),
]
