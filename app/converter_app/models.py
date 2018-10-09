from django.db import models


class CurrencyRate(models.Model):
    base_currency = models.CharField(max_length=3)
    convertible_currency = models.CharField(max_length=3)
    value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
