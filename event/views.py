from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from event.lib.t_core_scheduler import TradeScheduler
from event.models import TradeSuiteEvent


class EventListView(LoginRequiredMixin, TemplateView):
    template_name = "event_start.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = list(TradeSuiteEvent.objects.all())
        return context


class SchedulerStartView(LoginRequiredMixin, TemplateView):
    template_name = "scheduler_start.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trade_scheduler = TradeScheduler()
        return context

