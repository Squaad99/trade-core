import pytz
from datetime import datetime
from avz_client.avz_client import AvzClient
from event.lib.events import buy_and_place_orders
from event.models import TradeSuiteEvent


def test_job():
    job_name = "Test check"
    now_datetime = datetime.now(pytz.timezone('Europe/Stockholm'))
    now_full = str(now_datetime)
    now_date = now_datetime.strftime("%Y-%m-%d")
    now_time = now_datetime.strftime("%H:%M")

    trade_suit_event_list = TradeSuiteEvent.objects.filter(name=job_name, date=now_date, time_started=now_time)
    if trade_suit_event_list:
        return

    trade_suite_event = TradeSuiteEvent(name=job_name,
                                        date=now_date,
                                        time_started=now_time,
                                        time_completed=now_time,
                                        custom_full=now_full,
                                        test_data=True)

    trade_suite_event.save()


def health_check_job():
    job_name = "Health check"
    now_datetime = datetime.now(pytz.timezone('Europe/Stockholm'))
    now_full = str(now_datetime)
    now_date = now_datetime.strftime("%Y-%m-%d")
    now_time = now_datetime.strftime("%H:%M")

    trade_suit_event_list = TradeSuiteEvent.objects.filter(name=job_name, date=now_date, time_started=now_time)
    if trade_suit_event_list:
        return

    trade_suite_event = TradeSuiteEvent(name=job_name,
                                        date=now_date,
                                        time_started=now_time,
                                        time_completed=now_time,
                                        custom_full=now_full,
                                        test_data=False)
    trade_suite_event.save()


def buy_and_place_orders_job():
    job_name = "Buy and place orders"
    now_datetime = datetime.now(pytz.timezone('Europe/Stockholm'))
    now_full = str(now_datetime)
    now_date = now_datetime.strftime("%Y-%m-%d")
    now_time = now_datetime.strftime("%H:%M")

    trade_suit_event_list = TradeSuiteEvent.objects.filter(name=job_name, date=now_date, time_started=now_time, test_mode=False)
    if trade_suit_event_list:
        return

    trade_suite_event = TradeSuiteEvent(name=job_name,
                                        date=now_date,
                                        time_started=now_time,
                                        time_completed=now_time,
                                        custom_full=now_full,
                                        test_mode=False)
    trade_suite_event.save()

    result = "success"
    exception = ""
    try:
        avz_client = AvzClient()
        buy_and_place_orders(avz_client, trade_suite_event)
    except Exception as error:
        result = "failure"
        exception = str(error)

    done_datetime = datetime.now(pytz.timezone('Europe/Stockholm'))
    done_time = done_datetime.strftime("%H:%M")
    trade_suite_event.time_completed = done_time
    trade_suite_event.result = result
    trade_suite_event.error = exception
    trade_suite_event.save()


def check_transactions_and_orders_job():
    job_name = "Check transactions and orders"
    now_datetime = datetime.now(pytz.timezone('Europe/Stockholm'))
    now_full = str(now_datetime)
    now_date = now_datetime.strftime("%Y-%m-%d")
    now_time = now_datetime.strftime("%H:%M")

    trade_suit_event_list = TradeSuiteEvent.objects.filter(name=job_name, date=now_date, time_started=now_time)
    if trade_suit_event_list:
        return

    trade_suite_event = TradeSuiteEvent(name=job_name,
                                        date=now_date,
                                        time_started=now_time,
                                        time_completed=now_time,
                                        custom_full=now_full,
                                        test_data=False)
    trade_suite_event.save()
