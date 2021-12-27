from django.contrib import admin

# Register your models here.
from event.models import TradeSuiteEvent, Scheduler
from order.models import *
from stock.models import Stock
from strategy.models import StockStrategy, StrategyCriteria

admin.site.register(Stock)
admin.site.register(TradeSuiteEvent)
admin.site.register(StockStrategy)
admin.site.register(StrategyCriteria)
admin.site.register(BuyTransaction)
admin.site.register(SellTransaction)
admin.site.register(Order)
admin.site.register(Scheduler)