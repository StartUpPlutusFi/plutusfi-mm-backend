from django.urls import path
from apps.bid.api import views

app_name = "bid"

urlpatterns = [
    path("add", views.BidAdd.as_view(), name="bidAdd"),
    path("list", views.BidList.as_view(), name="bidList"),
    path("ctrl/<int:pk>", views.BidCtrl.as_view(), name="botCtrl"),
    path("detail/<int:pk>", views.BidDetail.as_view(), name="bidDetail"),
    path("delete/<int:pk>", views.BidDelete.as_view(), name="bidDelete"),
    path("update/<int:pk>", views.BidUpdate.as_view(), name="bidUpdate"),
    path("status/<int:pk>", views.BidStatus.as_view(), name="bidStatus"),
]
