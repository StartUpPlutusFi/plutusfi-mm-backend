from django.urls import path
from apps.bid.api import views

app_name = "bid"

urlpatterns = [
    path("list", views.BidList.as_view(), name="bidList"),
    path("add", views.BidAdd.as_view(), name="bidAdd"),
    # path("detail/<int:pk>/", views.bidDetails, name="bidDetails"),
    # path("update/<int:pk>/", views.bidUpdate, name="bidUpdate"),
    # path("delete/<int:pk>/", views.bidDelete, name="bidDelete"),
    # path("ctrl/<int:pk>/", views.bid_bot_ctrl, name="bidCtrl"),
    # path("status/<int:pk>/", views.bid_bot_run_status, name="bidStatus"),
    # path("buy/<int:pk>/", views.bid_bot_buy, name="bidBuy"),
    # path("cancel/<int:pk>/", views.bid_bot_cancel, name="bidCancel"),
]
