from django.contrib import admin
from .models import Exchange, BinanceAssetsControl

# Register your models here.
admin.site.register(BinanceAssetsControl)
admin.site.register(Exchange)
