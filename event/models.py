from django.db import models


class TradeSuiteEvent(models.Model):
    name = models.CharField(max_length=100, default="Automatic trade event")
    time_started_st = models.DateTimeField(default=None, null=True, blank=True)
    time_completed_st = models.DateTimeField(default=None, null=True, blank=True)
    date_started = models.CharField(max_length=50, default='')
    time_started = models.CharField(max_length=50, default='')
    result = models.CharField(max_length=50, default="")
    error = models.CharField(max_length=2000, default="")
    number_of_stocks = models.FloatField(default=0)
    number_of_orders = models.FloatField(default=0)
    number_of_buy_transactions = models.FloatField(default=0)
    number_of_sell_transactions = models.FloatField(default=0)
    test_mode = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
