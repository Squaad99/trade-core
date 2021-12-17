from avz_client.avz_client import AvzClient
from borsdata.borsdata_client import BorsdataClient

client = BorsdataClient()
markets = client.borsdata.get_markets()
selected_exchanges = ["OMX Stockholm"]
selected_markets = ["Large Cap"]
market_list = []
for market in markets:
    if market.name in selected_markets and market.exchangeName in selected_exchanges:
        market_list.append(market)

instrument_list = []
market_ids = []

for market in market_list:
    market_ids.append(market.id)


instrument_list = client.borsdata.get_instruments(market_ids)

#
# for instrument in instrument_list:
#     existing_stock = Stock.objects.filter(name=instrument.name)
#     if not existing_stock:
#         new_stock = Stock.objects.create(name=instrument.name, ticker=instrument.ticker)
#         new_stock.save()
