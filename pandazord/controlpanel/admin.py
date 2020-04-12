from django.contrib import admin
from .models import Exchange, BinanceAssetsControl, BinanceBackingTestAcquisition

# Register your models here.
admin.site.register(Exchange)
admin.site.register(BinanceAssetsControl)
admin.site.register(BinanceBackingTestAcquisition)
