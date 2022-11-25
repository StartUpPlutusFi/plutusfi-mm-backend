from django.urls import path
from apps.orderLimit.api import views

app_name = "orderLimit"

urlpatterns = [
    path("add", views.OrderLimitAdd.as_view(), name="OrderLimitAdd"),
    path("list", views.OrderLimitList.as_view(), name="OrderLimitList"),
    path(
        "ctrl/<int:pk>/<str:set>", views.OrderLimitCtrl.as_view(), name="OrderLimitCtrl"
    ),
    path("detail/<int:pk>", views.OrderLimitDetail.as_view(), name="OrderLimitDetail"),
    path("delete/<int:pk>", views.OrderLimitDelete.as_view(), name="OrderLimitDelete"),
    path("update/<int:pk>", views.OrderLimitUpdate.as_view(), name="OrderLimitUpdate"),
    path("status/<int:pk>", views.OrderLimitStatus.as_view(), name="OrderLimitStatus"),
]
