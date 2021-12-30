from avz_client.AVZ_VARS import BUY_AMOUNT
from avz_client.avz_client import AvzClient
from order.models import Order


def place_market_order_stop_loss_and_sell(ticker, avz_client: AvzClient, production, test_mode=False):
    buy_transaction = avz_client.buy_stock_market_price(ticker, 4000, production, test_mode)
    buy_price = buy_transaction.price
    decimals = str(buy_price)[::-1].find('.')

    profit_target = buy_price * 1.02
    profit_target = round(profit_target, decimals)
    lose_target = buy_price * 0.98
    lose_target = round(lose_target, decimals)

    if production:
        print("Not implemented")
        # Should place stop lose profit take and stop loss lose take

    order = Order(
        asset_ticker=ticker,
        completed=False,
        production=production,
        buy_transaction=buy_transaction,
        profit_target=profit_target,
        lose_target=lose_target
    )


    if not test_mode:

        order.save()



