from django.db import models
from django.utils.timezone import now


# Create your models here.

class TradeSuiteEvent(models.Model):
    name = models.CharField(max_length=30, default="Automatic trade event")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
