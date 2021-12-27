from django.db import models
from django.utils.timezone import now


# Create your models here.

class TradeSuiteEvent(models.Model):
    name = models.CharField(max_length=30, default="Automatic trade event")
    custom_date = models.CharField(max_length=50, default="Date to compare with")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Scheduler(models.Model):
    name = models.CharField(max_length=30, default="Scheduler status")
    last_started = models.CharField(max_length=50)
