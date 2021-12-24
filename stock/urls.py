from django.urls import path

from borsdata.STOCK_CONFIG import STOCK_LIST
from borsdata.borsdata_client import BorsdataClient
from manage import RUN_MODE
from stock.models import Stock
from stock.views import StockListView, StockDetail

urlpatterns = [
    path('', StockListView.as_view(), name='stock-list'),
    path('<int:pk>/', StockDetail.as_view(), name='stock-detail'),
]

if RUN_MODE:
    client = BorsdataClient()
    markets = client.borsdata.get_markets()
    selected_exchanges = ["OMX Stockholm"]
    selected_markets = ["Large Cap"]
    large_cap_exclude = ["ATCO A", "CORE A", "CORE D", "ELUX A", "EPI A", "ERIC A", "ESSITY A", "FPAR PREF", "SHB A",
                             "HOLM A", "HUSQ A", "INDU A", "INVE A", "KINV A", "NCC A", "KLED", "NENT A", "RATO A", "SCA A",
                             "SEB A", "SKF A", "SSAB A", "SAGA A", "SAGA D", "SBB D", "SDIP PREF", "STE A", "SWEC A",
                             "TEL2 A", "VOLV A", "FPAR A", "CORE PREF"]
    market_list = []
    for market in markets:
        if market.name in selected_markets and market.exchangeName in selected_exchanges:
            market_list.append(market)

    instrument_list = []
    market_ids = []

    for market in market_list:
        market_ids.append(market.id)


    instrument_list = client.borsdata.get_instruments(market_ids)

    for instrument in instrument_list:
        existing_stock = Stock.objects.filter(name=instrument.name, ticker=instrument.ticker)
        if not existing_stock and instrument.ticker not in large_cap_exclude:
            new_stock = Stock.objects.create(name=instrument.name, ticker=instrument.ticker)
            new_stock.save()

    for ticker in large_cap_exclude:
        existing_stock_exclude = Stock.objects.filter(ticker=ticker)
        existing_stock_exclude.delete()

