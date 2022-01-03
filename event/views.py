
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django_q.brokers import get_broker
from django_q.cluster import monitor
from django_q.models import Schedule
from django_q.monitor import info, get_ids
from django_q.status import Stat
import socket

from event.models import TradeSuiteEvent
from order.models import Order, BuyTransaction, SellTransaction


class EventListView(LoginRequiredMixin, TemplateView):
    template_name = "event_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_list = list(TradeSuiteEvent.objects.all())
        event_list.reverse()
        context['events'] = event_list
        return context


class TestEventsView(LoginRequiredMixin, TemplateView):
    template_name = "test_events.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        command = context['command']

        if command == "buy-and-sell":
            job_name = "Test Buy and sell"
            Schedule.objects.filter(name=job_name).delete()

            buy_and_sell_test_schedule = Schedule(name=job_name,
                                                  func='event.tasks.buy_and_place_orders_job',
                                                  schedule_type=Schedule.ONCE,
                                                  repeats=1,
                                                  args="'test'")
            buy_and_sell_test_schedule.save()
        elif command == "test-check-order-and-transactions":
            job_name = "Test Check orders and transactions"
            Schedule.objects.filter(name=job_name).delete()

            buy_and_sell_test_schedule = Schedule(name=job_name,
                                                  func='event.tasks.check_transactions_and_orders_job',
                                                  schedule_type=Schedule.ONCE,
                                                  repeats=1,
                                                  args="'test'")
            buy_and_sell_test_schedule.save()
        elif command == "clear-test-data":
            TradeSuiteEvent.objects.filter(test_mode=True).delete()
            Order.objects.filter(test_mode=True).delete()
            BuyTransaction.objects.filter(test_mode=True).delete()
            SellTransaction.objects.filter(test_mode=True).delete()

        return context
