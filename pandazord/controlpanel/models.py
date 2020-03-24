from django.db import models
from django.contrib.postgres.fields import JSONField
#from datetime import datetime

# Create your models here.

TRADE_CHOICES=(
    ('Y', 'yes'),
    ('N', 'no'),
)

default_signal_generator_parameters = {
    'name' : 'SimpleMovingAverageCrossOver',
    
    'parameters' : {
        'smaller_SMA' : {
            'n_samples' : 3,
            'candle_interval' : '1h',
            'price_source' : 'ohlc4'
        },

        'bigger_SMA' : {
            'n_samples' : 100,
            'candle_interval' : '1h',
            'price_source' : 'ohlc4'
        }
    }
}

default_stop_loss_parameters = {
    'name' : 'Default',
    
    'parameters': {
        'first_trigger' : {
            'candle_interval': '1m',
            'price_source' : 'ohlc4',               
            'rate(%)' : 5,
            'treshold' : {
                'n_measurements' : 10,
                'n_positives' : 3
            }
        },
        
        'second_trigger' : {
            'candle_interval': '1m',
            'price_source' : 'ohlc4',  
            'rate(%)' : 1,
            'treshold' : {
                'n_measurements' : 50,
                'n_positives' : 20
            }                
        },
        
        'update_target_if' : {
            'candle_interval': '1m',
            'price_source' : 'ohlc4',  
            'rate(%)' : 6,
            'treshold' : {
                'n_measurements' : 10,
                'n_positives' : 4                
            }
        }
    }
}

default_position_parameters = {
    'side' : 'closed',
    'size': 0.0,
    'target_price': 0.0
}

class Default:
    def signal_generator():
        return default_signal_generator_parameters
    
    def stop_loss():
        return default_stop_loss_parameters

    def position():
        return default_position_parameters


class AssetsControl(models.Model):

    asset_symbol = models.CharField(max_length=8, primary_key=True)
    trade_on = models.CharField(max_length=3, choices=TRADE_CHOICES, default='N')
    available_amount = models.FloatField(null=True, blank=True, default=0.0)
    signal_parameters = JSONField(default=Default.signal_generator)
    stop_parameters = JSONField(default=Default.stop_loss)
    position = JSONField(default=Default.position)
    
    class Meta:
        abstract = True

    def __str__(self):
        return self.asset_symbol

class BinanceAssetsControl(AssetsControl):
    class Meta:
        db_table = '"assets_control_binance"'
        verbose_name = "Binance"
        verbose_name_plural = "Binance"