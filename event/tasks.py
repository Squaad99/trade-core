import pytz

from datetime import datetime

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
                                        custom_full=now_full)
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
                                        custom_full=now_full)
    trade_suite_event.save()



def buy_and_place_orders_job():
    job_name = "Buy and place orders"
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
                                        custom_full=now_full)
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
                                        custom_full=now_full)
    trade_suite_event.save()