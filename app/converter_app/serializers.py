from rest_framework import serializers

from converter.enviroments import CURRENCIES
from converter_app.models import CurrencyRate


class CurrencyConversionSerializer(serializers.Serializer):
    base_currency = serializers.ChoiceField(choices=CURRENCIES)
    convertible_currency = serializers.ChoiceField(choices=CURRENCIES)
    amount = serializers.FloatField(min_value=0)


class CurrencyRateSerializer(serializers.ModelSerializer):
    def validate(self, data):
        data = super().validate(data)

        if data['base_currency'] == data['convertible_currency']:
            raise serializers.ValidationError(
                'Base currency code cannot equal to convertible'
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
