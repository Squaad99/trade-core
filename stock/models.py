from django.db import models

# Create your models here.
from django.db import models


class Stock(models.Model):
    name = models.CharField(max_length=30)
    ticker = models.CharField(max_length=30)

    def __str__(self):
        return self.name


