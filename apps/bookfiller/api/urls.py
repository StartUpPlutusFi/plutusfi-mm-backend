from django.urls import path
from apps.bookfiller.api import views

app_name = "bookfiller"

urlpatterns = [
    path("add", views.BookFillerAdd.as_view(), name="BookFillerAdd"),
    path("list", views.BookFillerList.as_view(), name="BookFillerList"),
    path("ctrl/<int:pk>", views.BookFillerCtrl.as_view(), name="BookFillerCtrl"),
    path("detail/<int:pk>", views.BookFillerDetail.as_view(), name="BookFillerDetail"),
    path("delete/<int:pk>", views.BookFillerDelete.as_view(), name="BookFillerDelete"),
    path("update/<int:pk>", views.BookFillerUpdate.as_view(), name="BookFillerUpdate"),
    path("status/<int:pk>", views.BookFillerStatus.as_view(), name="BookFillerStatus"),
    path("status/cancel_code/<int:pk>", views.BookFillerCancelCode.as_view(), name="BookFillerCancelCode"),
]
