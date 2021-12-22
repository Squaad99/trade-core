import sys

import pytz
from django.urls import path
from event.models import TradeSuiteEvent
from event.views import EventStartView
import threading
from datetime import datetime

import schedule
import time

urlpatterns = [
    path('start/<str:command>', EventStartView.as_view(), name='event-start'),
]


class TCoreScheduler:

    def __init__(self):
        def test_job():
            time_zone = pytz.timezone('Europe/Stockholm')
            trade_suite_event = TradeSuiteEvent(name="Manual testing", custom_date=str(datetime.now(time_zone)))
            trade_suite_event.save()

        # schedule.every(10).seconds.do(test_job)

    def start(self):
        print("Starting scheduler")

        def start_scheduler():
            while 1:
                schedule.run_pending()
                time.sleep(1)

        thread = threading.Thread(target=start_scheduler, args=[])
        thread.start()


args = sys.argv

if "collectstatic" not in args and "makemigrations" not in args and "migrate" not in args:
    s = TCoreScheduler()
    s.start()
