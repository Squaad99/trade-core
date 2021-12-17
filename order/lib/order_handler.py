from avz_client.AVZ_VARS import BUY_AMOUNT
from avz_client.avz_client import AvzClient


def place_market_order_stop_loss_and_sell(ticker, avz_client: AvzClient):
    if not avz_client.is_market_open() and not avz_client.check_available_balance(BUY_AMOUNT) and not avz_client.check_if_position_or_order_exist(ticker):
        return

    try:
        avz_client.buy_stock_market_price(ticker, 4000)
    except Exception as e:
        print(e)
