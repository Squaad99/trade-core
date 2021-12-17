import datetime
import os
from datetime import date

from avanza import Avanza, OrderType

from w_trade.data.price_data import PriceData


class AvzClient:

    def __init__(self):
        avz_u = os.environ.get('AVZ_U')
        avz_p = os.environ.get('AVZ_P')
        avz_topt = os.environ.get('AVZ_TOPT')

        # Trading account
        self.trade_account_id = '2425827'

        self.client = Avanza({
            'username': '{}'.format(avz_u),
            'password': '{}'.format(avz_p),
            'totpSecret': '{}'.format(avz_topt)
        })

    def get_stock_id(self, ticker):
        search_result = self.client.search_for_stock(ticker)
        for hit in search_result['hits']:
            for topHit in hit['topHits']:
                if topHit['flagCode'] == 'SE' and topHit['tickerSymbol'] == ticker:
                    return hit['topHits'][0]['id']

        return None

    def get_price_data_current_day(self, ticker, index):
        stock_id = self.get_stock_id(ticker)
        info = self.client.get_stock_info(stock_id)
        return PriceData(info['lastPrice'], info['lowestPrice'], info['highestPrice'], info['lowestPrice'],
                         info['lastPriceUpdated'], info['totalVolumeTraded'], index)

    def get_account_balance(self):
        account_overview = self.client.get_account_overview(self.trade_account_id)
        return account_overview['totalBalance']

    def buy_stock_market_price(self, ticker, amount_sek):
        stock_id = self.get_stock_id(ticker)
        info = self.client.get_stock_info(stock_id)
        sell_price = info['sellPrice']
        amount = int(amount_sek / sell_price)

        # result = self.client.place_order(
        #     account_id=self.trade_account_id,
        #     order_book_id=stock_id,
        #     order_type=OrderType.BUY,
        #     price=sell_price,
        #     valid_until=date.today(),
        #     volume=amount
        # )
        #
        # if result['status'] == "SUCCESS":
        #     print("dd")


        # response = {'status': 'SUCCESS', 'messages': [''], 'requestId': '-1', 'orderId': '396285491'}

        response = {'status': 'SUCCESS', 'messages': [''], 'orderId': '397233009', 'requestId': '-1'}

        order_id = response['orderId']
        deals_and_orders = self.client.get_deals_and_orders()
        for deal in deals_and_orders['deals']:
            if order_id == deal['orderId']:
                price = deal['price']
                volume = deal['volume']

    def get_order(self, order_id):
        dd = self.client.get_deals_and_orders()
        result = self.client.get_order(self.trade_account_id, order_id)

    def is_market_open(self):
        try:
            response = self.client.get_stock_info("5364")
            last_price_updated = response['lastPriceUpdated']
            last_price_updated = last_price_updated.split('+')[0]
            last_price_updated_datetime = datetime.datetime.strptime(last_price_updated, '%Y-%m-%dT%H:%M:%S.%f')
            current_time = datetime.datetime.now()

            delta = current_time - last_price_updated_datetime
            minutes = (delta.seconds // 60) % 60
            if minutes < 5:
                return True
        except Exception:
            return False
        return False

    def logout(self):
        self.client._session.close()

    def check_available_balance(self, amount):
        overview = self.client.get_account_overview(self.trade_account_id)
        available_balance = overview['totalBalance']
        if available_balance > amount:
            return True
        return False

    def check_if_position_or_order_exist(self, ticker):
        account_positions = self.client.get_accounts_positions()
        selected_id = self.get_stock_id(ticker)
        for position in account_positions['withOrderbook']:
            account_id = position['account']['id']
            stock_id = position['instrument']['orderbook']['id']
            if account_id == self.trade_account_id and selected_id == stock_id:
                return True
        deals_and_orders = self.client.get_deals_and_orders()
        for order in deals_and_orders['orders']:
            account_id = order['account']['id']
            stock_id = order['orderbook']['id']
            if account_id == self.trade_account_id and selected_id == stock_id:
                return True
        return False

    def place_stop_loss_sell_order(self):
        list_dd = self.client.get_all_stop_losses()
        self.client.place_order()

