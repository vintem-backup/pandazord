from django.db import models

#TODO: Docstrings and Type annotations

class PriceSeriesFrom:
    
    def __init__(self, market_df):
        
        super().__init__()
        self.market_df = market_df
    
    def open_(self):
        return self.market_df['open']
    
    def high_(self):
        return self.market_df['high']
    
    def low_(self):
        return self.market_df['low']
    
    def close_(self):
        return self.market_df['close']
    
    def ohlc4_(self):
        
        price = (self.market_df['open'] +
                self.market_df['high'] +
                self.market_df['low'] +
                self.market_df['close'])/4
        
        return price
    
    def hl2_(self):
        
        price = (self.market_df['high'] +
                self.market_df['low'])/2
        
        return price
    
    def hlc3_(self):
        
        price = (self.market_df['high'] +
                self.market_df['low'] +
                self.market_df['close'])/3
        
        return price