from django.urls import path
from apps.bid.api import views

app_name = "bidbot"

urlpatterns = [
    path("add", views.BidAdd.as_view(), name="BidAdd"),
    path("list", views.BidList.as_view(), name="BidList"),
    path("ctrl/<int:pk>", views.BidCtrl.as_view(), name="BidCtrl"),
    path("detail/<int:pk>", views.BidDetail.as_view(), name="BidDetail"),
    path("delete/<int:pk>", views.BidDelete.as_view(), name="BidDelete"),
    path("update/<int:pk>", views.BidUpdate.as_view(), name="BidUpdate"),
    path("status/<int:pk>", views.BidStatus.as_view(), name="BidStatus"),
]
