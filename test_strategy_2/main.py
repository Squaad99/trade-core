from borsdata.borsdata_client import BorsdataClient
from test_strategy.constants import *
from test_strategy.utils import get_start_date, check_trade_status
from test_strategy_2.data_set_2 import DataSet2
from test_strategy_2.strategy_2 import StrategyTwo
from w_trade.data.price_data import PriceData

TEST_PERIOD_LENGTH = 60
DATA_SET_COUNT = 0
STRATEGY = StrategyTwo()


def check_trade_status(low, high):
    if low < STRATEGY.lose_target:
        return TRADE_RESULT_LOSS
    elif high > STRATEGY.profit_target:
        return TRADE_RESULT_PROFIT
    return TRADE_RESULT_ONGOING


def check_strategy(data_set: DataSet2):
    STRATEGY.set_data_set(data_set)

    if STRATEGY.active_trade:
        trade_status = check_trade_status(data_set.low, data_set.high)
        if trade_status == TRADE_RESULT_LOSS:
            STRATEGY.finish_trade(STRATEGY.lose_target)
        elif trade_status == TRADE_RESULT_PROFIT:
            STRATEGY.finish_trade(STRATEGY.profit_target)
        STRATEGY.current_trade_length += 1
    else:
        strategy_filled = STRATEGY.check_criteria()
        if strategy_filled:
            STRATEGY.start_trade()


def loop_price_data(full_price_data, max_index):
    max_index_reached = False

    loop_times = (len(full_price_data) - 1) - TEST_PERIOD_LENGTH + 2
    for current_index in range(0, loop_times):
        end_index = TEST_PERIOD_LENGTH + current_index
        price_data = full_price_data[current_index:end_index]
        data_set = DataSet2(price_data)
        check_strategy(data_set)

        if data_set.index == max_index:
            max_index_reached = True
    return max_index_reached


def start_loop_instruments(instrument_list, borsdata_client):
    start_date = get_start_date(365)
    for instrument in instrument_list:
        full_price_data: [PriceData] = borsdata_client.get_daily_prices(instrument, start_date)
        max_index = len(full_price_data) - 1
        result = loop_price_data(full_price_data, max_index)
        if not result:
            print("All did not run :" + instrument.name)
        STRATEGY.reset_strategy()


def evaluate_strategy():
    STRATEGY.set_strategy_result()
    print(STRATEGY.name)
    print("Total trades: {}".format(STRATEGY.total_trades))
    print("Profit trades: {}".format(STRATEGY.total_trades_profit))
    print("Loss trades: {}".format(STRATEGY.total_trades_loses))
    print("Capital: {}".format(STRATEGY.start_capital))
    print("  --------------  ")

    if not STRATEGY.total_trades == 0:
        win_percentage = STRATEGY.total_trades_profit / STRATEGY.total_trades
        win_percentage = win_percentage * 100
        win_percentage = round(win_percentage, 2)
        print(win_percentage)


def run_complete_test():
    borsdata_client = BorsdataClient()
    instrument_list = borsdata_client.get_large_cap_instruments()
    start_loop_instruments(instrument_list, borsdata_client)
    evaluate_strategy()


run_complete_test()
