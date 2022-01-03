import enum


class EventEnum(enum.Enum):
    BUY_AND_PLACE_ORDERS = "Buy and place orders"
    CHECK_TRANSACTIONS_AND_ORDERS = "Check transactions and orders"
    RESULT_SUCCESS = "Success"
    RESULT_FAILED = "Success"
    RESULT_ONGOING = "Ongoing"


class OrderEnum(enum.Enum):
    ORDER_ONGOING = "ONGOING"
    ORDER_COMPLETED = "COMPLETED"

