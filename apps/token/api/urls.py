from django.urls import path
from apps.token.api.views import *

app_name = "token"
urlpatterns = [
    path("list", TokenList.as_view(), name="TokenList"),
    path("add", TokenAdd.as_view(), name="TokenAdd"),
    path("detail/<int:pk>", TokenDetail.as_view(), name="TokenDetail"),
    path("delete/<int:pk>", TokenDelete.as_view(), name="TokenDelete"),
    path("update/<int:pk>", TokenUpdate.as_view(), name="TokenUpdate"),
]
