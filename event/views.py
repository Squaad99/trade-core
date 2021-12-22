from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from event.models import TradeSuiteEvent


class EventStartView(LoginRequiredMixin, TemplateView):
    template_name = "event_start.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = list(TradeSuiteEvent.objects.all())
        return context