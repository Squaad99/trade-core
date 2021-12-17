import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

from avz_client.avz_client import AvzClient
from borsdata.borsdata_client import BorsdataClient
from stock.models import Stock
from w_trade.w_trader import WTrader


class StockListView(LoginRequiredMixin, ListView):
    model = Stock
    template_name = "stock_list.html"
    ordering = ["name", "ticker"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stock_list = list(context['object_list'])
        borsdata_client = BorsdataClient()
        for stock in stock_list:
            stock.status = False
            result = borsdata_client.get_instrument_by_ticker(stock.ticker)
            if result is not None:
                stock.status = True
        return context


class StockDetail(LoginRequiredMixin, DetailView):
    model = Stock
    template_name = 'stock_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stock = context['object']
        avz_client = AvzClient()
        w_trader = WTrader(avz_client)
        data_set = w_trader.get_data_set(stock.ticker)

        days = []
        close_prices = []

        day_index = 0

        for price_data in data_set.data_set_list:
            days.append(day_index)
            close_prices.append(price_data.close)
            day_index += 1

        context['data_set'] = data_set

        context['days'] = days
        context['close_prices'] = close_prices

        positive_waves = data_set.waves.positive_waves
        positive_waves_dict = []
        for positive_wave in positive_waves:
            temp_wave = []
            for price_data in positive_wave.wave_list:
                temp_wave.append({"x": price_data.index, "y": price_data.close})
            positive_waves_dict.append(temp_wave)
        context['positive_waves_dict'] = positive_waves_dict

        negative_waves = data_set.waves.negative_waves
        negative_waves_dict = []
        for negative_wave in negative_waves:
            temp_wave = []
            for price_data in negative_wave.wave_list:
                temp_wave.append({"x": price_data.index, "y": price_data.close})
            negative_waves_dict.append(temp_wave)
        context['negative_waves_dict'] = negative_waves_dict

        avz_client.logout()
        dd = avz_client.client._session

        dd.close()

        return context
