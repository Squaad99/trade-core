import secrets

import pytz
from event.models import TradeSuiteEvent, Scheduler, TCoreScheduler
import threading
from datetime import datetime

import schedule
import time


class TradeScheduler(object):

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
        print("Starting scheduler")
        scheduler_list = TCoreScheduler.objects.filter(name="T Scheduler status")
        code = str(secrets.token_urlsafe(13))

        if not scheduler_list:
            last_changed = datetime.now(self.time_zone)
            last_changed = str(last_changed).split('+')[0]
            new_scheduler = TCoreScheduler(last_updated=last_changed, scheduler_code=code)
            new_scheduler.save()
            time.sleep(1)


        def start_scheduler():
            while True:
                active_scheduler = TCoreScheduler.objects.get(name="T Scheduler status")

                if active_scheduler.scheduler_code != code:
                    break

                last_updated = datetime.now(self.time_zone)
                last_updated = str(last_updated).split('+')[0]
                active_scheduler.last_updated = last_updated
                active_scheduler.save()


                schedule.run_pending()
                time.sleep(10)


        thread = threading.Thread(target=start_scheduler, args=[])
        thread.start()
