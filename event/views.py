from datetime import datetime

import pytz
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from avz_client.avz_client import AvzClient
from event.lib.events import buy_and_place_orders
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


class SchedulerStartView(LoginRequiredMixin, TemplateView):
    template_name = "scheduler_start.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        TradeSuiteEvent.objects.filter(name="Test check").delete()
        return context


class TestEventsView(LoginRequiredMixin, TemplateView):
    template_name = "test_events.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        command = context['command']

        if command == "buy-and-sell":
            now_datetime = datetime.now(pytz.timezone('Europe/Stockholm'))
            now_full = str(now_datetime)
            now_date = now_datetime.strftime("%Y-%m-%d")
            now_time = now_datetime.strftime("%H:%M")

            trade_suite_event = TradeSuiteEvent(name="Test Buy and Sell",
                                                date=now_date,
                                                time_started=now_time,
                                                time_completed=now_time,
                                                custom_full=now_full)

            result = "success"
            exception = ""
            try:
                avz_client = AvzClient()
                buy_and_place_orders(avz_client, trade_suite_event, True)
            except Exception as error:
                result = "failure"
                exception = str(error)

            done_datetime = datetime.now(pytz.timezone('Europe/Stockholm'))
            done_time = done_datetime.strftime("%H:%M")
            trade_suite_event.time_completed = done_time
            trade_suite_event.result = result
            trade_suite_event.error = exception
            trade_suite_event.save()
        elif command == "clear-test-data":
            TradeSuiteEvent.objects.filter(test_mode=True).delete()
            Order.objects.filter(test_mode=True).delete()
            BuyTransaction.objects.filter(test_mode=True).delete()
            SellTransaction.objects.filter(test_mode=True).delete()
        return context
