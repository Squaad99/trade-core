import pandas as pd

from w_trade.data.price_data import PriceData


class DataSet2:

    def __init__(self, price_data_list: [PriceData]):
        self.price_data_list = price_data_list
        self.data_frame = self._create_data_frane()
        self._set_current_values()

    def _create_data_frane(self):
        data = []

        for price_data in self.price_data_list:
            data.append(
                [
                    price_data.close,
                    price_data.open,
                    price_data.high,
                    price_data.low,
                    price_data.date,
                    price_data.volume,
                    price_data.index
                ]
            )
        self.data_frame = pd.DataFrame(data, columns=['close', 'open', 'high', 'low', 'date', 'volume', 'index'])
        self._add_rsi_to_data_frame()
        return self.data_frame

    def _add_rsi_to_data_frame(self):
        delta = self.data_frame['close'].diff()
        up = delta.clip(lower=0)
        down = -1 * delta.clip(upper=0)
        ema_up = up.ewm(com=14, adjust=False).mean()
        ema_down = down.ewm(com=14, adjust=False).mean()
        rs = ema_up / ema_down
        self.data_frame['rsi'] = 100 - (100 / (1 + rs))

    def _add_volume_avg(self):
        print("")

    def _set_current_values(self):
        last_row = self.data_frame.iloc[-1]
        self.close = last_row['close']
        self.open = last_row['open']
        self.rsi = last_row['rsi']
        self.volume = last_row['volume']
        self.index = last_row['index']
        self.date = last_row['date']
        self.low = last_row['low']
        self.high = last_row['high']
        self.positive_day = False
        if self.close > self.open:
            self.positive_day = True
