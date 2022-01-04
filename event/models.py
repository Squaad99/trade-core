from django.db import models


class TradeSuiteEvent(models.Model):
    name = models.CharField(max_length=100, default="Automatic trade event")
    result = models.CharField(max_length=50, default="")
    error = models.CharField(max_length=2000, default="")
    number_of_stocks = models.FloatField(default=0)
    number_of_orders = models.FloatField(default=0)
    number_of_buy_transactions = models.FloatField(default=0)
    number_of_sell_transactions = models.FloatField(default=0)
    test_mode = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
