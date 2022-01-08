import statistics

from w_trade.data.constants import *
from w_trade.data.negative_wave import NegativeWave
from w_trade.data.positive_wave import PositiveWave
from w_trade.data.price_data import PriceData
from w_trade.variables import NEGATIVE, POSITIVE


class Waves:

    def __init__(self, data_set: [PriceData]):
        self.wave_minimum_length = 2
        self.data_set = data_set
        self.max_index = len(self.data_set)
        self.positive_waves = self._get_positive_waves()
        self._set_positive_wave_stats()
        self.negative_waves = self._get_negative_waves()
        self._set_negative_wave_stats()
        self.total_amount = self.negative_waves_amount + self.positive_waves_amount
        self.all_waves = self._get_full_list()
        self._set_all_waves_stats()
        self.last_wave_type = self._get_last_wave()
        self.current_wave = self._get_current_wave()
        self.last_3 = self._last_3_days()

    def _get_positive_waves(self):
        wave_list = []

        current_wave_list = []
        wave_length = 0

        for index, price_data in enumerate(self.data_set):
            if price_data not in current_wave_list:
                current_wave_list.append(price_data)
            next_index = (index + 1)
            if next_index >= len(self.data_set):
                break

            next_price_data = self.data_set[next_index]

            if price_data.close < next_price_data.close:
                current_wave_list.append(next_price_data)
                wave_length += 1
            else:
                if wave_length >= self.wave_minimum_length:
                    wave_list.append(PositiveWave(current_wave_list))
                current_wave_list = []
                wave_length = 0

        if wave_length >= self.wave_minimum_length:
            wave_list.append(PositiveWave(current_wave_list))

        return wave_list

    def _get_negative_waves(self):
        wave_list = []

        current_wave_list = []
        wave_length = 0

        for index, price_data in enumerate(self.data_set):
            if price_data not in current_wave_list:
                current_wave_list.append(price_data)
            next_index = (index + 1)
            if next_index >= len(self.data_set):
                break

            next_price_data = self.data_set[next_index]

            if price_data.close > next_price_data.close:
                current_wave_list.append(next_price_data)
                wave_length += 1
            else:
                if wave_length >= self.wave_minimum_length:
                    wave_list.append(NegativeWave(current_wave_list))
                current_wave_list = []
                wave_length = 0

        if wave_length >= self.wave_minimum_length:
            wave_list.append(NegativeWave(current_wave_list))

        return wave_list

    def _get_full_list(self):
        complete_list = self.positive_waves + self.negative_waves
        complete_list.sort(key=lambda x: x.start_index)
        return complete_list

    def _set_positive_wave_stats(self):
        self.positive_waves_amount = len(self.positive_waves)

        length_list = []
        change_percent_list = []

        for positive_wave in self.positive_waves:
            length_list.append(positive_wave.length)
            change_percent_list.append(positive_wave.change_percent)

        self.positive_median_length = round(statistics.median(length_list), 2)
        self.positive_average_length = round(statistics.mean(length_list), 2)
        self.positive_average_percent_change = round(statistics.mean(change_percent_list), 2)

    def _set_negative_wave_stats(self):
        self.negative_waves_amount = len(self.negative_waves)

        length_list = []
        change_percent_list = []

        for negative_wave in self.negative_waves:
            length_list.append(negative_wave.length)
            change_percent_list.append(negative_wave.change_percent)

        self.negative_median_length = round(statistics.median(length_list), 2)
        self.negative_average_length = round(statistics.mean(length_list), 2)
        self.negative_average_percent_change = round(statistics.mean(change_percent_list), 2)

    def _set_all_waves_stats(self):
        negative_after_positive = 0
        positive_after_positive = 0

        positive_after_negative = 0
        negative_after_negative = 0
        earlier_wave = None
        for wave in self.all_waves:
            if earlier_wave is not None:
                earlier_wave_type = POSITIVE
                if isinstance(earlier_wave, NegativeWave):
                    earlier_wave_type = NEGATIVE

                current_wave_type = POSITIVE
                if isinstance(wave, NegativeWave):
                    current_wave_type = NEGATIVE

                if earlier_wave_type == POSITIVE:
                    if current_wave_type == POSITIVE:
                        positive_after_positive += 1
                    elif current_wave_type == NEGATIVE:
                        negative_after_positive += 1
                elif earlier_wave_type == NEGATIVE:
                    if current_wave_type == POSITIVE:
                        positive_after_negative += 1
                    elif current_wave_type == NEGATIVE:
                        negative_after_negative += 1

            earlier_wave = wave

        total_after_positive = negative_after_positive + positive_after_positive
        result = (negative_after_positive / total_after_positive) * 100
        self.negative_after_positive_chance = round(result, 2)
        result = (positive_after_positive / total_after_positive) * 100
        self.positive_after_positive_chance = round(result, 2)

        total_after_negative = positive_after_negative + negative_after_negative
        result = (negative_after_negative / total_after_negative) * 100
        self.negative_after_negative_chance = round(result, 2)
        result = (positive_after_negative / total_after_negative) * 100
        self.positive_after_negative_chance = round(result, 2)

    def _get_last_wave(self):
        self.last_wave = self.all_waves[-1]
        if type(self.last_wave) is PositiveWave:
            self.last_wave_length = self.last_wave.length
            self.last_wave_change = self.last_wave.change_percent
            return POSITIVE_WAVE_TYPE
        elif type(self.last_wave) is NegativeWave:
            self.last_wave_length = self.last_wave.length
            self.last_wave_change = self.last_wave.change_percent
            return NEGATIVE_WAVE_TYPE
        return NEUTRAL_WAVE_TYPE

    def _get_current_wave(self):
        if self.last_wave.end_index == self.max_index:
            if type(self.last_wave) is PositiveWave:
                self.current_wave_length = self.last_wave.length
                self.current_wave_length = self.last_wave.change_percent
                return POSITIVE_WAVE_TYPE
            elif type(self.last_wave) is NegativeWave:
                self.current_wave_length = self.last_wave.length
                self.current_wave_change = self.last_wave.change_percent
                return NEGATIVE_WAVE_TYPE
        return NEUTRAL_WAVE_TYPE

    def _last_3_days(self):
        last_3 = self.data_set[-3:]
        first = last_3[0].close
        second = last_3[1].close
        third = last_3[2].close

        if first < second < third:
            return POSITIVE_WAVE_TYPE
        elif first > second > third:
            return NEGATIVE_WAVE_TYPE
        return NEUTRAL_WAVE_TYPE











