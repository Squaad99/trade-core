from test_strategy.utils import *
from w_trade.data.constants import NEGATIVE_WAVE_TYPE, POSITIVE_WAVE_TYPE
from w_trade.data.data_set_offline import DataSetOffline


class StrategyOne:

    def __init__(self):
        self.data_set_offline = None
        self.name = "Buy after negative wave if positive change above 80%. Negative longer than average"
        self.total_trades = 0
        self.total_trades_profit = 0
        self.total_trades_loses = 0
        self.uncompleted = 0
        self.active_trade = False
        self.profit_target = None
        self.lose_target = None
        self.current_trade_length = 0
        self.trade_days_length_list = []

    def set_data_set(self, data_set_offline: DataSetOffline):
        self.data_set_offline = data_set_offline

    def add_trade(self, buy_price):
        self.active_trade = True
        self.profit_target = get_profit_target_value(buy_price)
        self.lose_target = get_lose_target_value(buy_price)
        self.total_trades += 1

    def add_profit_trade(self):
        self.active_trade = False
        self.profit_target = None
        self.lose_target = None
        self.total_trades_profit += 1
        self.trade_days_length_list.append(self.current_trade_length)
        self.current_trade_length = 0

    def add_lose_trade(self):
        self.active_trade = False
        self.profit_target = None
        self.lose_target = None
        self.total_trades_loses += 1
        self.trade_days_length_list.append(self.current_trade_length)
        self.current_trade_length = 0

    def reset_strategy(self):
        self.active_trade = False
        self.profit_target = None
        self.lose_target = None

    def check_strategy(self):
        count = 0

        if self.data_set_offline.waves.positive_after_negative_chance > 75:
            count += 1

        if self.data_set_offline.waves.last_wave_type == NEGATIVE_WAVE_TYPE:
            count += 1

        #if self.data_set_offline.waves.last_wave_length > self.data_set_offline.waves.negative_average_length:
        #    count += 1

        if self.data_set_offline.waves.last_wave_change < self.data_set_offline.waves.negative_average_percent_change:
            count += 1

        # wave_type = self.data_set_offline.waves.current_wave
        # if wave_type == NEGATIVE_WAVE_TYPE:
        #     count += 1
        #
        #     current_wave_length = self.data_set_offline.waves.current_wave_length
        #     avg_negative_length = self.data_set_offline.waves.negative_average_length
        #     if current_wave_length > avg_negative_length:
        #         count += 1

        if count == 3:
            return True
        return False
