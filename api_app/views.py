import pytz
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

from event.lib.constants import EventCodes
from event.models import TradeSuiteEvent


class TestApiView(APIView):
    def post(self, request):
        payload = request.data
        event = payload['event']
        code = payload['code']

        time_zone = pytz.timezone('Europe/Stockholm')

        if event == EventCodes.TEST_NAME.value and code == "123":
            trade_suite_event = TradeSuiteEvent(name="Manual testing", custom_date=str(datetime.now(time_zone)))
            trade_suite_event.save()
        elif event == EventCodes.BUY_SELL_NAME.value and code == EventCodes.BUY_SELL_CODE.value:
            trade_suite_event = TradeSuiteEvent(name="Buy and sell", custom_date=str(datetime.now(time_zone)))
            trade_suite_event.save()
        elif event == EventCodes.CHECK_TRADES_NAME.value and code == EventCodes.CHECK_TRADES_CODE.value:
            trade_suite_event = TradeSuiteEvent(name="Check orders", custom_date=str(datetime.now(time_zone)))
            trade_suite_event.save()

        return Response({"status": "success"}, status=status.HTTP_200_OK)
