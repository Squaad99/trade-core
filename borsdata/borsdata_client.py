import os
from datetime import datetime, timedelta, date
from borsdata_sdk import BorsdataAPI

from w_trade.data.price_data import PriceData


class BorsdataClient:

    def __init__(self):
        self.borsdata = BorsdataAPI(os.environ.get('BORS_API_KEY'))
        self.instrument_list = None
        self.sectors = None

    def get_instrument_by_ticker(self, ticker):
        if not self.instrument_list:
            self.instrument_list = self.borsdata.get_instruments()
        for instrument in self.instrument_list:
            if instrument.ticker.lower() == ticker.lower():
                return instrument
        return None

    def get_latest_price(self, stock_id):
        entries = self.borsdata.get_instrument_stock_price(stock_id)
        last_entry = entries[-1]
        return last_entry.c

    def get_instruments_by_branch(self, branch_id):
        instrument_list = []

        if not self.instrument_list:
            self.instrument_list = self.borsdata.get_instruments()

        for instrument in self.instrument_list:
            if instrument.branchId == branch_id:
                instrument_list.append(instrument)
        return instrument_list

    def get_latest_price_by_ticker(self, ticker, current_last_price):
        print(ticker)
        instrument = self.get_instrument_by_ticker(ticker)
        if instrument is None:
            return current_last_price
        now = datetime.now()
        end_date_string = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
        start_date = now - timedelta(days=10)
        start_date_string = str(start_date.year) + "-" + str(start_date.month) + "-" + str(start_date.day)
        try:
            entries = self.borsdata.get_instrument_stock_price(instrument.insId, start=start_date_string,
                                                               end=end_date_string)
            last_entry = entries[-1]
            return last_entry.c
        except:
            return 0

    def get_sector_by_ticker(self, ticker):
        instrument = self.get_instrument_by_ticker(ticker)
        if not instrument:
            return "Missing"

        if not self.sectors:
            self.sectors = self.borsdata.get_sectors()
        for sector in self.sectors:
            if sector.id == instrument.sectorId:
                return sector.name

        return "Missing"

    def get_list(self, markets, exchanges):
        all_markets = self.borsdata.get_markets()
        selected_markets = []
        for market in all_markets:
            if market.name in markets and market.exchangeName in exchanges:
                selected_markets.append(market)
        return selected_markets

    def get_instruments_by_markets(self, markets):
        market_ids = []
        for market in markets:
            market_ids.append(market.id)
        return self.borsdata.get_instruments(market_ids)

    def get_daily_prices(self, instrument, start_date=None):
        current_date = date.today()
        if start_date:
            first_date = start_date
        else:
            data_period = 90
            first_date = current_date - timedelta(days=data_period)
            first_date.strftime("%d-%m-%Y")

        stock_prices = self.borsdata.get_instrument_stock_price(instrument.insId, str(first_date), str(current_date))
        data_set_list = []
        index = 0
        for stock_price in stock_prices:
            data_set_list.append(PriceData(stock_price, index))
            index += 1
        return data_set_list

    def get_large_cap_instruments(self):
        markets = self.borsdata.get_markets()
        selected_exchanges = ["OMX Stockholm"]
        selected_markets = ["Large Cap"]
        large_cap_exclude = ["ATCO A", "CORE A", "CORE D", "ELUX A", "EPI A", "ERIC A", "ESSITY A", "FPAR PREF",
                             "SHB A",
                             "HOLM A", "HUSQ A", "INDU A", "INVE A", "KINV A", "NCC A", "KLED", "NENT A", "RATO A",
                             "SCA A",
                             "SEB A", "SKF A", "SSAB A", "SAGA A", "SAGA D", "SBB D", "SDIP PREF", "STE A", "SWEC A",
                             "TEL2 A", "VOLV A", "FPAR A", "CORE PREF"]

        market_list = []
        for market in markets:
            if market.name in selected_markets and market.exchangeName in selected_exchanges:
                market_list.append(market)

        market_ids = []

        for market in market_list:
            market_ids.append(market.id)

        instrument_list = self.borsdata.get_instruments(market_ids)

        selected_instrument_list = []

        for instrument in instrument_list:
            if instrument.ticker not in large_cap_exclude:
                selected_instrument_list.append(instrument)

        return selected_instrument_list
