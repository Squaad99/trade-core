from avz_client.AVZ_VARS import BUY_AMOUNT
from avz_client.avz_client import AvzClient


def place_market_order_stop_loss_and_sell(ticker, avz_client: AvzClient, production):
    buy_transaction = avz_client.buy_stock_market_price(ticker, 4000, production)



