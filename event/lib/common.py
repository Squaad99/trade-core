from event.lib.constants import RESULT_ONGOING
from event.models import TradeSuiteEvent


def get_test_mode(mode_str):
    test_mode = False
    if mode_str == "test":
        test_mode = True
    return test_mode


def create_trade_suite_event(name: str, test_mode: str):
    trade_suite_event = TradeSuiteEvent(name=name, test_mode=test_mode, result=RESULT_ONGOING)
    trade_suite_event.save()
    return trade_suite_event


def update_trade_suite_event(trade_suite_event: TradeSuiteEvent,
                             number_of_orders,
                             number_of_stocks,
                             number_of_buy_transactions,
                             number_of_sell_transactions):
    trade_suite_event.number_of_orders = number_of_orders
    trade_suite_event.number_of_stocks = number_of_stocks
    trade_suite_event.number_of_buy_transactions = number_of_buy_transactions
    trade_suite_event.number_of_sell_transactions = number_of_sell_transactions
    trade_suite_event.save()


def result_trade_suite_event(trade_suite_event: TradeSuiteEvent, result, error=""):
    print("result " + result)
    trade_suite_event.result = result
    trade_suite_event.error = error
    trade_suite_event.save()
