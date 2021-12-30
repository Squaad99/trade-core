from django.urls import path
from order.views import OrderListView, BuyTransactionsListView

urlpatterns = [
    path('order-list/', OrderListView.as_view(), name='order-list'),
    path('buy-transaction-list/', BuyTransactionsListView.as_view(), name='buy-transaction-list'),
]