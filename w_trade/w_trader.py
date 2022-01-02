from avz_client.avz_client import AvzClient
from borsdata.borsdata_client import BorsdataClient
from w_trade.data.data_set import DataSet
from w_trade.data.price_data import PriceData


class WTrader:

    def __init__(self, avz_client: AvzClient):
        self.borsdata_client = BorsdataClient()
        self.avz_client = avz_client
        self.data_set = None

    def get_data_list(self, instrument_list):
        data_sets = []
        for instrument in instrument_list:
            data_sets.append(DataSet(instrument, self.borsdata_client, self.avz_client))
        return data_sets

    def get_data_set(self, ticker):
        instrument = self.borsdata_client.get_instrument_by_ticker(ticker)
        return DataSet(instrument, self.borsdata_client, self.avz_client)

    def get_data_list_by_stock_list(self, stock_list):
        data_sets = []
        for stock in stock_list:
            instrument = self.borsdata_client.get_instrument_by_ticker(stock.ticker)
            data_sets.append(DataSet(instrument, self.borsdata_client, self.avz_client))
        return data_sets

    def get_result_set(self, ticker, start_date):
        instrument = self.borsdata_client.get_instrument_by_ticker(ticker)
        data_set_list: [PriceData] = self.borsdata_client.get_daily_prices(instrument, start_date)
        return data_set_list
