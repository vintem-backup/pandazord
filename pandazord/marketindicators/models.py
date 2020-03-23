from django.db import models

#TODO: Docstrings and Type annotations

from .common_libs import PriceSeriesFrom

class Trend:

    def __init__(self, klines):

        self.klines = klines


    def simple_moving_average(self, price_source, number_of_samples):

        price = getattr(PriceSeriesFrom(self.klines), price_source + '_')()

        return price.rolling(number_of_samples).mean()


class Momentum:
    pass


class Volatility:
    pass


class Volume:
    pass
