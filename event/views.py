from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from avz_client.avz_client import AvzClient
from event.lib.events import buy_and_place_orders
from event.models import TradeSuiteEvent


class EventListView(LoginRequiredMixin, TemplateView):
    template_name = "event_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = list(TradeSuiteEvent.objects.all()).reverse()
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
        avz_client = AvzClient()
        buy_and_place_orders(avz_client, True)
        return context
