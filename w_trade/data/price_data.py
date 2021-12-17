from borsdata_sdk.models import StockPrice


class PriceData:

    def __init__(self, *args):
        if len(args) > 4:
            self.close = args[0]
            self.open = args[1]
            self.high = args[2]
            self.low = args[3]
            self.date = args[4]
            self.volume = args[5]
            self.index = args[6]
        else:
            self.close = args[0].c
            self.open = args[0].o
            self.high = args[0].h
            self.low = args[0].l
            self.date = args[0].d
            self.volume = args[0].v
            self.index = args[1]

    # def __init__(self, close, open_price, high, low, date, volume, index=None):
    #     self.close = close
    #     self.open = open_price
    #     self.high = high
    #     self.low = low
    #     self.date = date
    #     self.volume = volume
    #     self.index = index
