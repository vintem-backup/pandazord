#TODO: Docstrings and Type annotations

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from marketindicators.models import *

CANDLE_INTERVAL_CHOICES = (
    ('1m','1 minute'),
    ('3m','3 minutes'),
    ('5m','5 minutes'),
    ('15m','15 minutes'),
    ('30m','30 minutes'),
    ('1h','1 hour'),
    ('2h','2 hours'),
    ('4h','4 hours'),
    ('6h','6 hours'),
    ('12h','12 hours'),
    ('1d','1 day'),
    ('1w','1 week'),
    ('1M','1 month'),
)

PRICE_SOURCE_CHOICES = (
    ('O','Open'),
    ('H','High'),
    ('L','Low'),
    ('C','Close'),
    ('OHLC4','(O+H+L+C)/4'),
    ('HL2','(H+L)/2'),
    ('HLC3','(H+L+C)/3'),
)

class SimpleMovingAverageCrossOver(models.Model):
    
    class Meta:

        db_table = '"SMA_CrossOver"'
        verbose_name = "SMA CrossOver parameter"
        verbose_name_plural = "SMA CrossOver parameters"
    
    parameter_set_name = models.CharField(max_length=10, primary_key=True)
    
    candle_interval = models.CharField(max_length=3, choices=CANDLE_INTERVAL_CHOICES)
    
    n_smaller = models.IntegerField(
        default=3,
        validators=[MaxValueValidator(500), MinValueValidator(1)]
        )
    
    n_bigger = models.IntegerField(
        default=100,
        validators=[MaxValueValidator(500), MinValueValidator(1)]
        )
    
    price_source = models.CharField(max_length=5, choices=PRICE_SOURCE_CHOICES, default='OHLC4')
    
    def save(self, *args, **kwargs):
        if (self.n_bigger <= self.n_smaller):
            raise ValueError ("n_bigger must be greater then n_smaller")
        else:
            super().save(*args, **kwargs)
    
    def __str__(self):
        return self.parameter_set_name
        
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