from borsdata.borsdata_client import BorsdataClient
from test_strategy.constants import TRADE_RESULT_LOSS, TRADE_RESULT_PROFIT
from test_strategy.strategy import StrategyOne
from test_strategy.utils import get_start_date, check_trade_status
from w_trade.data.data_set_offline import DataSetOffline
from w_trade.data.price_data import PriceData

borsdata_client = BorsdataClient()
instrument_list = borsdata_client.get_large_cap_instruments()

strategy = StrategyOne()

start_date = get_start_date(365)
period_length = 60

dataset_count = 0

for instrument in instrument_list:
    strategy.reset_strategy()
    full_price_data: [PriceData] = borsdata_client.get_daily_prices(instrument, start_date)
    max_index = len(full_price_data) - 1
    loop_times = max_index - period_length + 2

    for index_add in range(0, loop_times):
        start_index = index_add
        end_index = period_length + index_add
        selected_price_data = full_price_data[start_index:end_index]
        dataset_count += 1

        if strategy.active_trade:
            current_price_data = full_price_data[(end_index - 1)]
            trade_status = check_trade_status(current_price_data, strategy.lose_target, strategy.profit_target)
            if trade_status == TRADE_RESULT_LOSS:
                strategy.add_lose_trade()
            elif trade_status == TRADE_RESULT_PROFIT:
                strategy.add_profit_trade()
            strategy.current_trade_length += 1
        else:
            selected_data_set = DataSetOffline(selected_price_data)
            strategy.set_data_set(selected_data_set)
            strategy_filled = strategy.check_strategy()
            if strategy_filled:
                strategy.add_trade(selected_data_set.close)


print("Dataset count: " + str(dataset_count))
print(strategy.name)
print("Total trades: {}".format(strategy.total_trades))
print("Profit trades: {}".format(strategy.total_trades_profit))
print("Loss trades: {}".format(strategy.total_trades_loses))
print("Loss trades: {}".format(strategy.trade_days_length_list))
print("  --------------  ")

if not strategy.total_trades == 0:
    win_percentage = strategy.total_trades_profit / strategy.total_trades
    win_percentage = win_percentage * 100
    win_percentage = round(win_percentage, 2)
    print(win_percentage)

# for strategy in strategy_list:
#     if strategy.active_trade:
#         current_price_data = full_price_data[(end_index - 1)]
#         trade_status = check_trade_status(current_price_data, strategy.lose_target, strategy.profit_target)
#         if trade_status == TRADE_RESULT_LOSS:
#             strategy.add_lose_trade()
#         elif trade_status == TRADE_RESULT_PROFIT:
#             strategy.add_profit_trade()
#         strategy.current_trade_length += 1
#     else:
#         selected_data_set = DataSetOffline(selected_price_data)
#         strategy.set_data_set(selected_data_set)
#         strategy_filled = strategy.check_strategy()
#         if strategy_filled:
#             strategy.add_trade(selected_data_set.close)
