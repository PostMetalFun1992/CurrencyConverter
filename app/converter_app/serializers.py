import os
from datetime import datetime

from django.utils import timezone
from rest_framework import serializers

from converter_app.models import CurrencyRate


RATES_UPDATE_PERIOD_DAYS = int(os.getenv('RATES_UPDATE_PERIOD_DAYS', '1'))


class CurrencyConversationSerializer(serializers.Serializer):
    base_currency = serializers.CharField(max_length=3)
    convertible_currency = serializers.CharField(max_length=3)
    amount = serializers.FloatField()


class CurrencyRateSerializer(serializers.ModelSerializer):
    def validate(self, data):
        data = super().validate(data)
        now = timezone.now()

        if CurrencyRate.objects.filter(
            base_currency=data['base_currency'],
            convertible_currency=data['convertible_currency'],
            created_at__gte=datetime(
                now.year, now.month, now.day, tzinfo=now.tzinfo
            )
        ).exists():
            raise serializers.ValidationError(
                'Latest currency rate {}-{} for period "{} {}" already exists'
                .format(
                    data['base_currency'],
                    data['convertible_currency'],
                    RATES_UPDATE_PERIOD_DAYS, 'Day'
                )
            )

        return data

    class Meta:
        model = CurrencyRate
        fields = (
            'id',
            'base_currency',
            'convertible_currency',
            'value',
            'created_at'
        )
