from datetime import date, timedelta

from test_strategy.constants import *
from w_trade.data.price_data import PriceData


def get_start_date(number_of_days=365):
    current_date = date.today()
    start_date = current_date - timedelta(days=number_of_days)
    start_date.strftime("%d-%m-%Y")
    return start_date


def get_profit_target_value(buy_price):
    decimals = str(buy_price)[::-1].find('.')
    profit_target = float(buy_price) * float(PROFIT_TARGET)
    profit_target = round(profit_target, decimals)
    return profit_target


def get_lose_target_value(buy_price):
    decimals = str(buy_price)[::-1].find('.')
    lose_target = float(buy_price) * float(LOSE_TARGET)
    lose_target = round(lose_target, decimals)
    return lose_target


def check_trade_status(price_data: PriceData, lose_target, profit_target):
    lowest_price = price_data.low
    highest_price = price_data.high
    if lowest_price < lose_target:
        return TRADE_RESULT_LOSS
    elif highest_price > profit_target:
        return TRADE_RESULT_PROFIT
    return TRADE_RESULT_ONGOING
