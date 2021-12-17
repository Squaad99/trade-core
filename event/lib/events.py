from avz_client.avz_client import AvzClient
from event.models import TradeSuiteEvent
from order.lib.order_handler import place_market_order_stop_loss_and_sell
from stock.models import Stock
from strategy.lib.criteria_check import check_all_criteria
from strategy.models import StockStrategy, StrategyCriteria
from w_trade.w_trader import WTrader


def check_strategies_auto():
    # trade_suite_event = TradeSuiteEvent()
    # trade_suite_event.save()

    strategies = list(StockStrategy.objects.all())
    for strategy in strategies:
        strategy_criteria_list = StrategyCriteria.objects.filter(stock_strategy__name=strategy.name)
        strategy.strategy_criteria_list = list(strategy_criteria_list)
    stocks = list(Stock.objects.all())

    avz_client = AvzClient()

    w_trader = WTrader(avz_client)
    data_set_list = w_trader.get_data_list_by_stock_list(stocks)

    # Go over each data set
    for data_set in data_set_list:
        # Check each strategy
        for strategy in strategies:
            criteria_list = strategy.strategy_criteria_list
            criteria_result = check_all_criteria(criteria_list, data_set)

            if criteria_result:
                place_market_order_stop_loss_and_sell(data_set.instrument.ticker)
