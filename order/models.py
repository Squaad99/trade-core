from django.db import models
from order.lib.ORDER_VARS import ORDER_ACTIVE
from order.lib.constants import Transactions


class BuyTransaction(models.Model):
    status = models.CharField(max_length=30, default=Transactions.ACTIVE)
    price = models.FloatField()
    amount = models.FloatField()
    order_id = models.CharField(max_length=30, blank=True)
    stop_loss_id = models.CharField(max_length=30, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)


class SellTransaction(models.Model):
    status = models.CharField(max_length=30, default=Transactions.ACTIVE)
    price = models.FloatField(default=None, blank=True)
    amount = models.FloatField()
    take_profit = models.FloatField()
    stop_loss = models.FloatField()
    order_id = models.CharField(max_length=30, blank=True)
    stop_loss_id = models.CharField(max_length=30, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)


class Order(models.Model):
    status = models.CharField(max_length=30, default=ORDER_ACTIVE)
    asset_ticker = models.CharField(max_length=30)
    completed = models.DateTimeField(auto_now_add=True)
    production = models.BooleanField(default=False)
    buy_transaction = BuyTransaction()
    buy_transaction = models.ForeignKey(BuyTransaction, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.asset_ticker
