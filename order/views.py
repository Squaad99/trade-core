from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from order.models import Order


class OrderListView(LoginRequiredMixin, TemplateView):
    template_name = "order_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_list = list(Order.objects.all())
        order_list.reverse()
        context['order_list'] = order_list
        return context