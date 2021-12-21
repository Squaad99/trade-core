import threading
from datetime import datetime

import pytz
import requests
import schedule
import time

from event.lib.constants import EventCodes


class TCoreScheduler:

    def __init__(self):
        def test_job():
            payload = {
                "event": EventCodes.TEST_NAME.value,
                "code": EventCodes.TEST_CODE.value
            }
            self._preform_api_call(payload)

        def buy_and_sell_job():
            payload = {
                "event": EventCodes.BUY_SELL_NAME.value,
                "code": EventCodes.BUY_SELL_CODE.value
            }
            self._preform_api_call(payload)

        def check_orders_and_transactions_job():
            payload = {
                "event": EventCodes.CHECK_TRADES_NAME.value,
                "code": EventCodes.CHECK_TRADES_CODE.value
            }
            self._preform_api_call(payload)

        #schedule.every(10).seconds.do(test_job)

        schedule.every().monday.at("16:00").do(buy_and_sell_job)
        schedule.every().tuesday.at("16:00").do(buy_and_sell_job)
        schedule.every().wednesday.at("16:00").do(buy_and_sell_job)
        schedule.every().thursday.at("16:00").do(buy_and_sell_job)
        schedule.every().friday.at("16:00").do(buy_and_sell_job)
        #
        schedule.every().monday.at("20:00").do(check_orders_and_transactions_job)
        schedule.every().tuesday.at("20:00").do(check_orders_and_transactions_job)
        schedule.every().wednesday.at("20:00").do(check_orders_and_transactions_job)
        schedule.every().thursday.at("20:00").do(check_orders_and_transactions_job)
        schedule.every().friday.at("20:00").do(check_orders_and_transactions_job)

    def start(self):
        print("Starting scheduler")

        def start_scheduler():
            while 1:
                schedule.run_pending()
                time.sleep(1)

        thread = threading.Thread(target=start_scheduler, args=[])
        thread.start()

    @staticmethod
    def _preform_api_call(payload):
        try:
            requests.post('http://localhost:8000/api/event-start/', data=payload)
        except Exception as e:
            print(e)
