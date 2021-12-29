import pytz

from event.models import TradeSuiteEvent
from datetime import datetime


def test_job():
    trade_suite_event = TradeSuiteEvent(name="Test check",
                                        custom_date=str(datetime.now(pytz.timezone('Europe/Stockholm'))))
    trade_suite_event.save()
