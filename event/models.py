from django.db import models


class TradeSuiteEvent(models.Model):
    name = models.CharField(max_length=30, default="Automatic trade event")
    custom_full = models.CharField(max_length=50, default='')
    date = models.CharField(max_length=50, default='')
    time_started = models.CharField(max_length=50, default='')
    time_completed = models.CharField(max_length=50, default="")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
