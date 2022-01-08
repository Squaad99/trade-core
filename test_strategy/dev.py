# total_trades = 5639
# positive_trades = 3029
# negative_trades = 2610
#
# win_percentage = positive_trades / total_trades
# win_percentage = win_percentage * 100
# win_percentage = round(win_percentage, 2)
# print(win_percentage)
from borsdata.borsdata_client import BorsdataClient

borsdata_client = BorsdataClient()
dd = borsdata_client.borsdata.get_sectors()
print("dd")