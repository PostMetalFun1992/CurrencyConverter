import os
from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models


RATES_UPDATE_PERIOD_DAYS = int(os.getenv('RATES_UPDATE_PERIOD_DAYS', '1'))


class CurrencyRate(models.Model):
    base_currency = models.CharField(max_length=3)
    convertible_currency = models.CharField(max_length=3)
    value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def validate_unique(self):
        super().validate_unique(self)
        now = datetime.now()

        if CurrencyRate.objects.filter(
            base_currency=self.base_currency,
            convertible_currency=self.convertible_currency,
            created_at__gte=datetime(now.year, now.month, now.day)
        ).exists():
            raise ValidationError(
                'Latest currency rate {}-{} for period "{} {}" already exists'
                .format(
                    self.base_currency, self.convertible_currency,
                    RATES_UPDATE_PERIOD_DAYS, 'Day'
                )
            )
