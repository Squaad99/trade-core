from avz_client.avz_client import AvzClient
from event.models import TradeSuiteEvent
from order.lib.ORDER_VARS import ORDER_ACTIVE
from order.lib.order_handler import place_market_order_stop_loss_and_sell
from order.models import Order
from stock.models import Stock
from strategy.lib.criteria_check import check_all_criteria
from strategy.models import StockStrategy, StrategyCriteria
from w_trade.w_trader import WTrader


def buy_and_place_orders(avz_client: AvzClient, trade_suite_event: TradeSuiteEvent, test_mode=False):
    market_open = avz_client.is_market_open()
    if not market_open and not test_mode:
        return

    strategies = list(StockStrategy.objects.all())
    for strategy in strategies:
        strategy_criteria_list = StrategyCriteria.objects.filter(stock_strategy__name=strategy.name)
        strategy.strategy_criteria_list = list(strategy_criteria_list)
    stocks = list(Stock.objects.all())
    trade_suite_event.number_of_stocks = len(stocks)

    w_trader = WTrader(avz_client)
    data_set_list = w_trader.get_data_list_by_stock_list(stocks)

    number_of_orders = 0

    # Go over each data set
    for data_set in data_set_list:
        # Check each strategy
        for strategy in strategies:
            criteria_list = strategy.strategy_criteria_list
            criteria_result = check_all_criteria(criteria_list, data_set)

            if criteria_result:
                place_market_order_stop_loss_and_sell(data_set.instrument.ticker,
                                                      avz_client,
                                                      strategy,
                                                      test_mode)
                number_of_orders += 1
    trade_suite_event.number_of_trades = number_of_orders


def check_order_and_transactions(avz_client: AvzClient, test_mode=False):
    active_orders = list(Order.objects.all(status=ORDER_ACTIVE))

    for order in active_orders:
        order_created = order.created

