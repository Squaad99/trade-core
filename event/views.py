from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django_q.models import Schedule

from event.lib.constants import *
from event.models import TradeSuiteEvent
from order.models import Order, BuyTransaction, SellTransaction


class EventListView(LoginRequiredMixin, TemplateView):
    template_name = "event_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        buy_and_sell_event_list = list(TradeSuiteEvent.objects.filter(name=BUY_AND_PLACE_ORDERS))
        buy_and_sell_event_list.reverse()
        context['buy_and_sell_event_list'] = buy_and_sell_event_list

        check_transactions_and_order_list = list(TradeSuiteEvent.objects.filter(name=CHECK_TRANSACTIONS_AND_ORDERS))
        check_transactions_and_order_list.reverse()
        context['check_transactions_and_order_list'] = check_transactions_and_order_list

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
