"""Neste módulo, estão os objetos responsáveis por controlar o operacional, dando ao usuário a possibilidade
de inserir e alterar alguns parâmetros.

"""

from django.db import models
from django.contrib.postgres.fields import JSONField
from datetime import datetime

# Create your models here.

TRADE_CHOICES=(
    ('Y', 'yes'),
    ('N', 'no'),
)

AUTO_UPDATE_CHOICES=(
    ('ON','on'),
    ('OFF','off'),
    )

default_requests_limits = {
    "sampling period" : "1m",
    "number of samples per request" : 500,
    "max requests per period" : 1200
}

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
    """Retorna valores  padrões de alguns campos
    
    """
    def signal_generator() -> dict:
        """Valores padrões para o signal_generator
        
        """
        return default_signal_generator_parameters
    
    def stop_loss() -> dict:
        """Valores padrões para o stop_loss
        
        """
        return default_stop_loss_parameters

    def position_details() -> dict:
        """Valores padrões para o position
        
        """
        return default_position_parameters
    
    def requests_limits() -> dict:
        """Valores padrões para o requests_limits
        
        """
        return default_requests_limits


class Exchange(models.Model):
    """Objeto django para listar as exchanges e as principais informações das mesmas.

    """
    name = models.CharField(max_length=15, primary_key=True)
    api_endpoint_main_url = models.URLField(max_length=200)
    requests_limits = JSONField(default=Default().requests_limits)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = '"exchanges_information"'
        verbose_name = "Exchange Info"
        verbose_name_plural = "Exchanges Info"


class AssetsControl(models.Model):
    """Classe pai das listas de ativos operados, e os parãmetros de controle das operações dos mesmos.

    """
    asset_symbol = models.CharField(max_length=8, primary_key=True)
    trade_on = models.CharField(max_length=3, choices=TRADE_CHOICES, default='N')
    available_amount = models.FloatField(null=True, blank=True, default=0.0)
    signal_parameters = JSONField(default=Default().signal_generator)
    stop_parameters = JSONField(default=Default().stop_loss)
    position = JSONField(default=Default().position_details)
    
    class Meta:
        abstract = True

    def __str__(self):
        return self.asset_symbol


class BackingTestAssetsAcquisition(models.Model):
    """Tabela (provisória) para controle da aquisição de dados para backingtest 
    
    """
    asset_symbol = models.CharField(max_length=8, primary_key=True)
    auto_update = models.CharField(max_length=3, choices=AUTO_UPDATE_CHOICES, default='OFF')
    status = models.CharField(max_length=8, default='absent')
    last_updated_by_pid = models.IntegerField(null=True, blank=True)
    collect_data_since = models.DateTimeField(default = datetime.fromtimestamp(1241893500))
    
    class Meta:
        abstract = True

    def __str__(self):
        return self.asset_symbol


class BinanceBackingTestAcquisition(BackingTestAssetsAcquisition):
    """Classe filha (provisória) para controle da aquisição de dados de backingtest da binance
    
    """
    class Meta:
        db_table = '"binance_BT_assets_control"'
        verbose_name = "Binance - Backing_Test Assets acquisition"
        verbose_name_plural = "Binance - Backing_Test Assets acquisition"


class BinanceAssetsControl(AssetsControl):
    """Classe filha dos ativos operados na binance

    """
    class Meta:
        db_table = '"assets_control_binance"'
        verbose_name = "Binance - Real Trade control by Assets"
        verbose_name_plural = "Binance - Real Trade control by Assets"