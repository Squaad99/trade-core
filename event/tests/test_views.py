from unittest import mock
from unittest.mock import MagicMock

from django.test import TestCase

from avz_client.avz_client import AvzClient
from event.lib.events import buy_and_place_orders
from event.models import TradeSuiteEvent




class BuyAndSellTest(TestCase):

    def setUp(self):
        self.trade_suite_event = TradeSuiteEvent.objects.create(name="Test Buy Sell",
                                                                custom_full="2021-12-29 16:00:16.603536+01:00",
                                                                date="2021-12-29",
                                                                time_started="16:00",
                                                                time_completed="16:00")



    def test_start_complete_test(self):
        avz_client = MagicMock()

        buy_and_place_orders(avz_client, self.trade_suite_event)

        print("dd")
