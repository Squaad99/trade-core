from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from strategy.models import StockStrategy, StrategyCriteria


class StrategyListView(LoginRequiredMixin, TemplateView):
    template_name = "strategy_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        strategy_list = list(StockStrategy.objects.all())
        strategy_list.reverse()

        for strategy in strategy_list:
            strategy.criteria_list = list(StrategyCriteria.objects.filter(stock_strategy=strategy.pk))


        context['strategy_list'] = strategy_list
        return context