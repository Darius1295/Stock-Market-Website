from django.db import models


class Share(models.Model):
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return self.symbol
#    open = models.FloatField()
#    high = models.FloatField()
#    low = models.FloatField()
#    price = models.FloatField()
#    volume = models.IntegerField()
#    prev_close = models.FloatField()