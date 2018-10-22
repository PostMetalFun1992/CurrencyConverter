from decimal import Decimal

from django.db import models


class CurrencyRate(models.Model):
    ONE_UNIT_RATE_VALUE = Decimal('1.00')
    QUANTIZE_VALUE = Decimal('1.000000')

    base_currency = models.CharField(max_length=3)
    convertible_currency = models.CharField(max_length=3)
    value = models.DecimalField(max_digits=16, decimal_places=6)
    created_at = models.DateTimeField(auto_now_add=True)
