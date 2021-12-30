from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from order.models import Order, BuyTransaction


class OrderListView(LoginRequiredMixin, TemplateView):
    template_name = "order_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_list = list(Order.objects.all())
        order_list.reverse()
        context['order_list'] = order_list
        return context


class BuyTransactionsListView(LoginRequiredMixin, TemplateView):
    template_name = "buy_transactions_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        buy_transaction_list = list(BuyTransaction.objects.all())
        buy_transaction_list.reverse()
        context['buy_transaction_list'] = buy_transaction_list
        return context
