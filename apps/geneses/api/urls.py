from django.urls import path
from apps.geneses.api.views import *

app_name = "geneses"

urlpatterns = [
    path("list", GenesesList.as_view(), name="GenesesList"),
    path("add", GenesesAdd.as_view(), name="GenesesAdd"),
    path("ctrl", GenesesAdd.as_view(), name="GenesesAdd"),
    path("detail/<int:pk>", GenesesDetail.as_view(), name="GenesesDetail"),
    path("delete/<int:pk>", GenesesDelete.as_view(), name="GenesesDelete"),
    path("update/<int:pk>", GenesesUpdate.as_view(), name="GenesesUpdate"),

]

