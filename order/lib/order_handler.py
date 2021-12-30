from avz_client.avz_client import AvzClient
from order.lib.constants import TradeSettings
from order.models import Order
from strategy.models import StockStrategy


def place_market_order_stop_loss_and_sell(ticker, avz_client: AvzClient, strategy: StockStrategy, test_mode=False):
    buy_transaction = avz_client.buy_stock_market_price(ticker, strategy.production, test_mode)
    buy_price = buy_transaction.price
    decimals = str(buy_price)[::-1].find('.')

    profit_target = float(buy_price) * float(TradeSettings.PROFIT_TARGET.value)
    profit_target = round(profit_target, decimals)
    lose_target = float(buy_price) * float(TradeSettings.LOSE_TARGET.value)
    lose_target = round(lose_target, decimals)

    if strategy.production:
        print("Not implemented")
        # Should place stop lose profit take and stop loss lose take

    order = Order(
        asset_ticker=ticker,
        strategy=strategy,
        production=strategy.production,
        buy_transaction=buy_transaction,
        profit_target=profit_target,
        lose_target=lose_target
    )


    if not test_mode:
        order.save()



