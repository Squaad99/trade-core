import enum


class Transactions(enum.Enum):
    ACTIVE = 'ACTIVE'
    COMPLETED = 'COMPLETED'


class TradeSettings(enum.Enum):
    PROFIT_TARGET = 1.02
    LOSE_TARGET = 0.98
    TRADE_AMOUNT = 2000
