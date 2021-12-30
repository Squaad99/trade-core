from avz_client.avz_client import AvzClient
from order.lib.ORDER_VARS import ORDER_ACTIVE
from order.lib.order_handler import place_market_order_stop_loss_and_sell
from order.models import Order
from stock.models import Stock
from strategy.lib.criteria_check import check_all_criteria
from strategy.models import StockStrategy, StrategyCriteria
from w_trade.w_trader import WTrader


def buy_and_place_orders(avz_client: AvzClient, test_mode=False):
    if not avz_client.is_market_open():
        return

    strategies = list(StockStrategy.objects.all())
    for strategy in strategies:
        strategy_criteria_list = StrategyCriteria.objects.filter(stock_strategy__name=strategy.name)
        strategy.strategy_criteria_list = list(strategy_criteria_list)
    stocks = list(Stock.objects.all())
    if test_mode:
        stocks = stocks[:2]

    w_trader = WTrader(avz_client)
    data_set_list = w_trader.get_data_list_by_stock_list(stocks)

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


def check_order_and_transactions(avz_client: AvzClient, test_mode=False):
    active_orders = list(Order.objects.all(status=ORDER_ACTIVE))

    for order in active_orders:
        order_created = order.created

        print("ii")

    print("dd")
