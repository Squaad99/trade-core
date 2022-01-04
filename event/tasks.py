from event.lib.common import get_test_mode, create_trade_suite_event, result_trade_suite_event, check_if_run_already
from event.lib.constants import *
from event.lib.events import buy_and_place_orders, check_order_and_transactions


def buy_and_place_orders_job(mode=""):
    test_mode = get_test_mode(mode)
    check_if_run_already(test_mode)
    trade_suite_event = create_trade_suite_event(BUY_AND_PLACE_ORDERS, test_mode)

    try:
        buy_and_place_orders(trade_suite_event, test_mode)
        result = RESULT_SUCCESS
        error = ""
    except Exception as e:
        error = str(e)
        result = RESULT_FAILED

    result_trade_suite_event(trade_suite_event, result, error)


def check_transactions_and_orders_job(mode=""):
    test_mode = get_test_mode(mode)
    check_if_run_already(test_mode)
    trade_suite_event = create_trade_suite_event(CHECK_TRANSACTIONS_AND_ORDERS, test_mode)

    try:
        check_order_and_transactions(trade_suite_event, test_mode)
        result = RESULT_SUCCESS
        error = ""
    except Exception as e:
        error = str(e)
        result = RESULT_FAILED

    result_trade_suite_event(trade_suite_event, result, error)
