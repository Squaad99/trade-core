from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from event.lib.events import check_strategies_auto
from event.models import TradeSuiteEvent
from strategy.models import StockStrategy


class EventStartView(LoginRequiredMixin, TemplateView):
    template_name = "event_start.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        command = kwargs['command']

        if command == "start-123" and self.request.user.is_authenticated:
            check_strategies_auto()

        return context