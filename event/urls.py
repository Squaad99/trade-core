import pytz
from django.urls import path
from event.models import TradeSuiteEvent
from event.views import EventStartView
import threading
from datetime import datetime

import schedule
import time

from manage import RUN_MODE

urlpatterns = [
    path('start/<str:command>', EventStartView.as_view(), name='event-start'),
]


class TCoreScheduler:

    def __init__(self):
        time_zone = pytz.timezone('Europe/Stockholm')

        def test_job():
            trade_suite_event = TradeSuiteEvent(name="Test check", custom_date=str(datetime.now(time_zone)))
            trade_suite_event.save()

        def health_check_job():
            trade_suite_event = TradeSuiteEvent(name="Health check", custom_date=str(datetime.now(time_zone)))
            trade_suite_event.save()


        def buy_and_sell_job():
            trade_suite_event = TradeSuiteEvent(name="Buy and sell", custom_date=str(datetime.now(time_zone)))
            trade_suite_event.save()

        def check_orders_and_transactions_job():
            trade_suite_event = TradeSuiteEvent(name="Check order and transactions", custom_date=str(datetime.now(time_zone)))
            trade_suite_event.save()

        #schedule.every().minute.do(test_job)

        schedule.every().day.at("11:00").do(health_check_job)

        schedule.every().monday.at("15:00").do(buy_and_sell_job)
        schedule.every().tuesday.at("15:00").do(buy_and_sell_job)
        schedule.every().wednesday.at("15:00").do(buy_and_sell_job)
        schedule.every().thursday.at("15:00").do(buy_and_sell_job)
        schedule.every().friday.at("15:00").do(buy_and_sell_job)

        schedule.every().monday.at("19:00").do(check_orders_and_transactions_job)
        schedule.every().tuesday.at("19:00").do(check_orders_and_transactions_job)
        schedule.every().wednesday.at("19:00").do(check_orders_and_transactions_job)
        schedule.every().thursday.at("19:00").do(check_orders_and_transactions_job)
        schedule.every().friday.at("19:00").do(check_orders_and_transactions_job)

    def start(self):
        print("Starting scheduler")

        def start_scheduler():
            while 1:
                schedule.run_pending()
                time.sleep(1)

        thread = threading.Thread(target=start_scheduler, args=[])
        thread.start()


if RUN_MODE:
    s = TCoreScheduler()
    s.start()
