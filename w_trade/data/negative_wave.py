from w_trade.data.calculator import get_percentage_diff


class NegativeWave:

    def __init__(self, wave_list):
        self.wave_list = wave_list
        self.length = len(self.wave_list)
        self.change_percent = - get_percentage_diff(self.wave_list[0].open, self.wave_list[-1].close)
        self._validate_wave()
        self.start_index = self.wave_list[0].index
        self.end_index = (self.start_index + self.length)

    def _validate_wave(self):
        for index, price_data in enumerate(self.wave_list):
            next_index = (index + 1)
            if next_index >= len(self.wave_list):
                break
            next_price_data = self.wave_list[next_index]

            if not next_price_data.close < price_data.close:
                raise ValueError("Wave error value not lower then previous")
