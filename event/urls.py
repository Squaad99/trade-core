import os

import pytz
from django.urls import path
from event.models import TradeSuiteEvent, Scheduler
from event.views import EventStartView
import threading
from datetime import datetime

import schedule
import time

from manage import RUN_MODE

urlpatterns = [
    path('start/<str:command>', EventStartView.as_view(), name='event-start'),
]


class TCoreScheduler(object):

    def __init__(self):
        self.running = False
        self.time_zone = pytz.timezone('Europe/Stockholm')

        def test_job():
            trade_suite_event = TradeSuiteEvent(name="Test check", custom_date=str(datetime.now(self.time_zone)))
            trade_suite_event.save()

        def health_check_job():
            trade_suite_event = TradeSuiteEvent(name="Health check", custom_date=str(datetime.now(self.time_zone)))
            trade_suite_event.save()

        def buy_and_sell_job():
            trade_suite_event = TradeSuiteEvent(name="Buy and sell", custom_date=str(datetime.now(self.time_zone)))
            trade_suite_event.save()

        def check_orders_and_transactions_job():
            trade_suite_event = TradeSuiteEvent(name="Check order and transactions",
                                                custom_date=str(datetime.now(self.time_zone)))
            trade_suite_event.save()

        TradeSuiteEvent.objects.exclude(name="Test check")


        schedule.every().minute.do(test_job)

        schedule.every().day.at("12:00").do(health_check_job)

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

        self._start()

    def _start(self):
        print("Running start")
        scheduler_list = Scheduler.objects.filter(name="Scheduler status")

        if not scheduler_list:
            started = datetime.now(self.time_zone)
            new_scheduler = Scheduler(last_started=started)
            new_scheduler.save()
            time.sleep(1)

        scheduler = Scheduler.objects.get(name="Scheduler status")

        current_time = datetime.now(self.time_zone)
        current_time = str(current_time).split('+')[0]
        current_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S.%f')

        last_started = str(scheduler.last_started).split('+')[0]
        last_started = datetime.strptime(last_started, '%Y-%m-%d %H:%M:%S.%f')
        print("time diff")
        print(current_time)
        print(last_started)

        time_difference = current_time - last_started
        minutes = (time_difference.seconds // 60) % 60

        if minutes < 5:
            return

        scheduler.last_started = datetime.now(self.time_zone)
        scheduler.save()



        print("Starting scheduler")
        print(str(datetime.now(self.time_zone)))

        def start_scheduler():
            while True:
                schedule.run_pending()
                time.sleep(1)

        thread = threading.Thread(target=start_scheduler, args=[])
        thread.start()


if RUN_MODE:
    scheduler = TCoreScheduler()
