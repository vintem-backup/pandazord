from django.db import models

#TODO: Docstrings and Type annotations

from .market_indicators import *


class CrossSMA:
    
    def __init__(self, parameters):
        
        self.n_smaller = parameters['n_smaller']
        self.n_bigger = parameters['n_bigger']
        self.price_source = parameters['price_source']

        
    def how_many_candles(self):
        
        return self.n_bigger


    def what_side_and_leverage(self, klines):
        
        side = 'short'; leverage = 1.0
        
        if (len(klines) < self.n_bigger):
            
            raise IndexError ('There os no sufficient klines entrys to calculate the bigger moving avarage')
        
        else:

            rolling_mean = Trend(klines).simple_moving_average
            last_smaller = rolling_mean(self.price_source, self.n_smaller)[len(klines) - 1]
            last_bigger = rolling_mean(self.price_source, self.n_bigger)[len(klines) - 1]
            
            if (last_smaller > last_bigger): side = 'long'
        
        return side, leverage

    def verify(self, klines, position):
        
        side, leverage = self.what_side_and_leverage(klines)
        
        class Trade:
            
            def __init__(self, position, side, leverage):
                
                self.is_true = False
                self.leverage = leverage
                self.command = 'hold'
                    
                if(side == 'long' and position['side'] == 'closed'): 
                    self.command = 'buy'; self.is_true = True
                
                elif(side == 'short' and position['side'] == 'long'): 
                    self.command = 'sell'; self.is_true = True
        
        return Trade(position, side, leverage)