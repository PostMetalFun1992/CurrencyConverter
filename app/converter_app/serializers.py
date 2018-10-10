from datetime import datetime

from django.utils import timezone
from rest_framework import serializers

from converter.enviroments import CURRENCIES, RATES_UPDATE_PERIOD_DAYS
from converter_app.models import CurrencyRate


class CurrencyConversationSerializer(serializers.Serializer):
    base_currency = serializers.ChoiceField(choices=CURRENCIES)
    convertible_currency = serializers.ChoiceField(choices=CURRENCIES)
    amount = serializers.FloatField(min_value=0)


class CurrencyRateSerializer(serializers.ModelSerializer):
    def validate(self, data):
        data = super().validate(data)
        now = timezone.now()

        if data['base_currency'] == data['convertible_currency']:
            raise serializers.ValidationError(
                'Base currency code cannot equal to convertible'
            )

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
