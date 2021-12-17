from django.contrib import admin

# Register your models here.
from event.models import TradeSuiteEvent
from stock.models import Stock
from strategy.models import StockStrategy, StrategyCriteria

admin.site.register(Stock)
admin.site.register(TradeSuiteEvent)
admin.site.register(StockStrategy)
admin.site.register(StrategyCriteria)