import enum
import secrets


class EventCodes(enum.Enum):
    TEST_NAME = "Test"
    TEST_CODE = secrets.token_urlsafe(13)

    BUY_SELL_NAME = "Buy-Sell"
    BUY_SELL_CODE = secrets.token_urlsafe(13)

    CHECK_TRADES_NAME = "Check-Trades"
    CHECK_TRADES_CODE = secrets.token_urlsafe(13)


class OrderEnum(enum.Enum):
    ORDER_ONGOING = "ONGOING"
    ORDER_COMPLETED = "COMPLETED"

