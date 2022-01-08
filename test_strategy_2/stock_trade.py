

class StockTrade:

    def __init__(self, buy_price, sell_price, days):
        self.buy_price = buy_price
        self.sell_price = sell_price
        self.days = days
        self.profitable = self._get_trade_profitable()

    def _get_trade_profitable(self):
        if self.sell_price > self.buy_price:
            return True
        return False
