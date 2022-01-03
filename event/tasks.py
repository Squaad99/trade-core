import pytz
from datetime import datetime
from avz_client.avz_client import AvzClient
from event.lib.constants import EventEnum
from event.lib.events import buy_and_place_orders, check_order_and_transactions
from event.models import TradeSuiteEvent


def buy_and_place_orders_job(mode=""):
    test_mode = False
    if mode == "test":
        test_mode = True

    now = datetime.now(pytz.timezone('Europe/Stockholm'))
    now_date = now.strftime("%Y-%m-%d")
    now_time = now.strftime("%H:%M")

    trade_suit_event_list = TradeSuiteEvent.objects.filter(name=EventEnum.BUY_AND_PLACE_ORDERS.value,
                                                           time_started=now_time,
                                                           date_started=now_date)
    if trade_suit_event_list:
        return

    trade_suite_event = TradeSuiteEvent(name=EventEnum.BUY_AND_PLACE_ORDERS.value,
                                        time_started_st=now,
                                        time_started=now_time,
                                        date_started=now_date,
                                        test_mode=test_mode,
                                        result=EventEnum.RESULT_ONGOING.value)
    trade_suite_event.save()

    exception = ""
    try:
        avz_client = AvzClient()
        buy_and_place_orders(avz_client, trade_suite_event, test_mode)
        result = EventEnum.RESULT_SUCCESS.value
    except Exception as error:
        exception = str(error)
        result = EventEnum.RESULT_FAILED.value

    done_datetime = datetime.now(pytz.timezone('Europe/Stockholm'))
    done_time = done_datetime.strftime("%H:%M")
    trade_suite_event.time_completed = done_time
    trade_suite_event.result = result
    trade_suite_event.error = exception
    trade_suite_event.save()


def check_transactions_and_orders_job(mode=""):
    test_mode = False
    if mode == "test":
        test_mode = True
    now = datetime.now(pytz.timezone('Europe/Stockholm'))
    now_date = now.strftime("%Y-%m-%d")
    now_time = now.strftime("%H:%M")

    trade_suit_event_list = TradeSuiteEvent.objects.filter(name=EventEnum.CHECK_TRANSACTIONS_AND_ORDERS.value,
                                                           date_started=now_date,
                                                           time_started=now_time)
    if trade_suit_event_list:
        return

    trade_suite_event = TradeSuiteEvent(name=EventEnum.CHECK_TRANSACTIONS_AND_ORDERS.value,
                                        time_started_st=now,
                                        date_started=now_date,
                                        time_started=now_time,
                                        test_mode=test_mode,
                                        result=EventEnum.RESULT_ONGOING.value)
    trade_suite_event.save()

    exception = ""
    try:
        avz_client = AvzClient()
        check_order_and_transactions(avz_client, trade_suite_event, test_mode)
        result = EventEnum.RESULT_SUCCESS.value
    except Exception as error:
        exception = str(error)
        result = EventEnum.RESULT_FAILED.value

    done_datetime = datetime.now(pytz.timezone('Europe/Stockholm'))
    trade_suite_event.time_completed_st = done_datetime
    trade_suite_event.result = result
    trade_suite_event.error = exception
    trade_suite_event.save()
