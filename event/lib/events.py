from avz_client.avz_client import AvzClient
from event.lib.common import update_trade_suite_event
from event.lib.constants import ORDER_ONGOING, ORDER_COMPLETED
from event.models import TradeSuiteEvent
from order.lib.order_handler import place_market_order_stop_loss_and_sell
from order.models import Order, SellTransaction
from stock.models import Stock
from strategy.lib.criteria_check import check_all_criteria
from strategy.models import StockStrategy, StrategyCriteria
from w_trade.w_trader import WTrader


def buy_and_place_orders(trade_suite_event: TradeSuiteEvent, test_mode=False):
    avz_client = AvzClient()
    market_open = avz_client.is_market_open()
    if not market_open and not test_mode:
        return

    strategies = list(StockStrategy.objects.all())
    for strategy in strategies:
        strategy_criteria_list = StrategyCriteria.objects.filter(stock_strategy__name=strategy.name)
        strategy.strategy_criteria_list = list(strategy_criteria_list)
    stocks = list(Stock.objects.all())

    w_trader = WTrader(avz_client)
    data_set_list = w_trader.get_data_list_by_stock_list(stocks)
    number_of_stocks = len(data_set_list)

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
    update_trade_suite_event(trade_suite_event, number_of_orders, number_of_stocks, number_of_orders, 0)


def check_order_and_transactions(trade_suite_event: TradeSuiteEvent, test_mode=False):
    avz_client = AvzClient()
    w_trader = WTrader(avz_client)
    active_orders = list(Order.objects.filter(status=ORDER_ONGOING))
    number_of_orders = len(active_orders)
    number_of_sell_transactions = 0

    for order in active_orders:
        order_created = order.created
        profit_target = order.profit_target
        lose_target = order.lose_target
        date_string = order_created.strftime("%Y-%m-%d")
        result_set = w_trader.get_result_set(order.asset_ticker, date_string)
        order_completed = False
        order_successful = True
        amount = order.buy_transaction.amount
        if order.test_mode:

            for i, price_data in enumerate(result_set):
                if i == 0:
                    close_price = price_data.close
                    if close_price < lose_target:
                        sell_transactions = SellTransaction(price=lose_target,
                                                            amount=amount,
                                                            order_id="",
                                                            test_mode=test_mode)
                        sell_transactions.save()
                        order_completed = True
                        order_successful = False
                    elif close_price > profit_target:
                        sell_transactions = SellTransaction(price=profit_target,
                                                            amount=amount,
                                                            order_id="",
                                                            test_mode=test_mode)
                        sell_transactions.save()
                        order_completed = True
                        order_successful = True
                else:
                    lowest_price = price_data.low
                    highest_price = price_data.high
                    if lowest_price < lose_target:
                        order_completed = True
                        order_successful = False
                        sell_transactions = SellTransaction(price=lose_target,
                                                            amount=amount,
                                                            order_id="",
                                                            test_mode=test_mode)
                        sell_transactions.save()
                    elif highest_price > profit_target:
                        sell_transactions = SellTransaction(price=profit_target,
                                                            amount=amount,
                                                            order_id="",
                                                            test_mode=test_mode)
                        sell_transactions.save()
                        order_completed = True
                        order_successful = True

            if order_completed:
                number_of_sell_transactions += 1

            if order_completed:
                order.status = ORDER_COMPLETED
                order.sell_transaction = sell_transactions
                order.successful = order_successful
                order.save()
        else:
            print("Implement real selling")

    update_trade_suite_event(trade_suite_event, number_of_orders, number_of_orders, 0, number_of_sell_transactions)
