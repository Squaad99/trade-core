from django.urls import path
from django_q.models import Schedule

from event.views import EventListView, SchedulerStartView, TestBuyAndSellView
from manage import RUN_MODE
from order.views import OrderListView

urlpatterns = [
    path('order-list/', OrderListView.as_view(), name='order-list'),
]