from datetime import timedelta as td

from django.utils import timezone as tz
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

        base = data['base_currency']
        convertible = data['convertible_currency']
        border = tz.now() - td(days=RATES_UPDATE_PERIOD_DAYS)

        if base == convertible:
            raise serializers.ValidationError(
                'Base currency code cannot equal to convertible'
            )

        rate_in_current_period = CurrencyRate.objects.filter(
            base_currency=base,
            convertible_currency=convertible,
        ).exclude(
            created_at__year=border.year,
            created_at__month=border.month,
            created_at__day=border.day,
        ).first()

        if rate_in_current_period:
            raise serializers.ValidationError(
                'Latest currency rate {}-{} for period "{} Day" already exists'
                .format(base, convertible, RATES_UPDATE_PERIOD_DAYS)
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
