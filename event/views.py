from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from avz_client.avz_client import AvzClient
from event.lib.events import buy_and_place_orders
from event.models import TradeSuiteEvent


class EventListView(LoginRequiredMixin, TemplateView):
    template_name = "event_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = list(TradeSuiteEvent.objects.all())
        return context


class SchedulerStartView(LoginRequiredMixin, TemplateView):
    template_name = "scheduler_start.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        TradeSuiteEvent.objects.filter(name="Test check").delete()
        return context



class TestBuyAndSellView(LoginRequiredMixin, TemplateView):
    template_name = "test_buy_sell.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trade_suite_event = TradeSuiteEvent.objects.create(name="Test Buy Sell",
                                                           custom_full="2021-12-29 16:00:16.603536+01:00",
                                                           date="2021-12-29",
                                                           time_started="16:00",
                                                           time_completed="16:00")

        avz_client = AvzClient()
        buy_and_place_orders(avz_client, trade_suite_event, True)
        return context
