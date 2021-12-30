from django.db import models
from order.lib.ORDER_VARS import ORDER_ACTIVE
from strategy.models import StockStrategy


class BuyTransaction(models.Model):
    price = models.FloatField()
    amount = models.FloatField()
    order_id = models.CharField(max_length=30, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)


class SellTransaction(models.Model):
    price = models.FloatField()
    amount = models.FloatField()
    order_id = models.CharField(max_length=30, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)


class Order(models.Model):
    status = models.CharField(max_length=30, default=ORDER_ACTIVE)
    asset_ticker = models.CharField(max_length=30)
    production = models.BooleanField(default=False)
    strategy = models.ForeignKey(StockStrategy, on_delete=models.CASCADE)
    buy_transaction = models.ForeignKey(BuyTransaction, on_delete=models.CASCADE, blank=True, default=None, null=True)
    sell_transaction = models.ForeignKey(SellTransaction, on_delete=models.CASCADE, blank=True, default=None, null=True)
    profit_target = models.FloatField(default=0)
    profit_stop_loss_id = models.CharField(default='', max_length=50)
    lose_target = models.FloatField(default=0)
    lose_stop_loss_id = models.CharField(default='', max_length=50)
    last_updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    dummy = models.CharField(default='', max_length=50)


    def __str__(self):
        return self.asset_ticker
