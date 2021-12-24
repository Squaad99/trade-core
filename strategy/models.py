from django.db import models


# Create your models here.

class StockStrategy(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    production = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class StrategyCriteria(models.Model):
    stock_strategy = models.ForeignKey(StockStrategy, on_delete=models.CASCADE)
    data_name = models.CharField(max_length=50)
    # Above, Under, Equal
    value_direction = models.CharField(max_length=50)
    value_selection = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.data_name