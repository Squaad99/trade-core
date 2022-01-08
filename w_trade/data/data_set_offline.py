import calendar
import datetime
from w_trade.data.calculator import get_percentage_diff
from w_trade.data.price_data import PriceData
from w_trade.data.waves import Waves


class DataSetOffline:

    def __init__(self, data_set_list):
        self.data_set_list: [PriceData] = data_set_list
        self.last_date = self.data_set_list[-1].date
        self.week_day = self._get_week_day()
        self.days = len(self.data_set_list)
        self.positive_days = self._get_positive_days()
        self.negative_days = self._get_negatives_days()
        self.change_percentage = self._get_change_percentage()
        if self.change_percentage > 0:
            self.positive_period = True
        else:
            self.positive_period = False
        self.waves = Waves(self.data_set_list)
        self._set_stats()

    def _get_positive_days(self):
        count = 0
        for price_set in self.data_set_list:
            if price_set.open > price_set.close:
                count += 1
        return count

    def _get_negatives_days(self):
        count = 0
        for price_set in self.data_set_list:
            if price_set.open < price_set.close:
                count += 1
        return count

    def _get_change_percentage(self):
        first = self.data_set_list[0]
        last = self.data_set_list[-1]
        self.open = first.open
        self.close = last.close
        return get_percentage_diff(self.open, self.close)

    def _set_stats(self):
        self.highest = self.data_set_list[0].high
        self.lowest = self.data_set_list[0].low

        for data in self.data_set_list:
            if data.low < self.lowest:
                self.lowest = data.low
            if data.high > self.highest:
                self.highest = data.high

        diff_low_high = self.highest - self.lowest
        each_point = diff_low_high / 100
        diff_low = self.close - self.lowest
        self.low_high_ratio = round((diff_low / each_point), 2)

    def _get_week_day(self):
        if "T" in self.last_date:
            self.last_date = self.last_date.split("T")[0]

        year, month, day = (int(x) for x in self.last_date.split('-'))
        ans = datetime.date(year, month, day)
        return calendar.day_name[ans.weekday()]
