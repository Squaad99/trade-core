from test_strategy.utils import *
from test_strategy_2.constants import TRADE_CAPITAL, EACH_TRADE
from test_strategy_2.data_set_2 import DataSet2
from test_strategy_2.stock_trade import StockTrade


class StrategyTwo:

    def __init__(self):
        self.data_set = None
        self.name = "Buy after negative wave if positive change above 80%. Negative longer than average"
        self.total_trades = 0
        self.total_trades_profit = 0
        self.total_trades_loses = 0
        self.uncompleted = 0
        self.active_trade = False
        self.buy_price = None
        self.profit_target = None
        self.lose_target = None
        self.current_trade_length = 0
        self.stock_trade_list = []
        self.start_capital = TRADE_CAPITAL

    def set_data_set(self, data_set: DataSet2):
        self.data_set = data_set

    def start_trade(self):
        self.active_trade = True
        self.buy_price = self.data_set.close
        self.profit_target = get_profit_target_value(self.buy_price)
        self.lose_target = get_lose_target_value(self.buy_price)
        self.total_trades += 1

    def finish_trade(self, sell_price):
        self.active_trade = False
        self.profit_target = None
        self.lose_target = None
        self.stock_trade_list.append(
            StockTrade(self.buy_price, sell_price, self.current_trade_length)
        )
        self.current_trade_length = 0
        self.buy_price = None

    def reset_strategy(self):
        self.active_trade = False
        self.profit_target = None
        self.lose_target = None
        self.current_trade_length = 0
        self.buy_price = None

    def check_criteria(self):
        count = 0
        
        if self.data_set.rsi < 35:
            count += 1

        if count == 1:
            return True
        return False

    def set_strategy_result(self):
        self.total_trades = len(self.stock_trade_list)

        for stock_trade in self.stock_trade_list:
            trade_amount = self.start_capital * EACH_TRADE
            trade_change = (stock_trade.sell_price / stock_trade.buy_price) - 1
            trade_change = round(trade_change, 3)
            trade_result = trade_amount * trade_change
            self.start_capital += trade_result

            if stock_trade.profitable:
                self.total_trades_profit += 1
            else:
                self.total_trades_loses += 1

