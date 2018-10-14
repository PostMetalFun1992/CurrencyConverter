from decimal import Decimal

from rest_framework import status
import requests as r

from converter.enviroments import CURRENCIES, RATES_API_URL
from converter_app.models import CurrencyRate
from converter_app.serializers import CurrencyRateSerializer


EQUAL_CODE_RATE_VALUE = 1.0


def compose_combinations(currencies=CURRENCIES):
    return {currency: currencies - {currency} for currency in currencies}


def get_currency_rates(base, convertibles):
    resp = r.get(RATES_API_URL, params={'base': base})

    if not resp.status_code == status.HTTP_200_OK:
        return {}

    rates = resp.json()['rates']

    return {currency: rates[currency] for currency in convertibles}


def get_currencies_rates():
    return {base: get_currency_rates(base, convertibles)
            for base, convertibles in compose_combinations().items()}


def upload_rates():
    rates = []
    for base, convertibles in get_currencies_rates().items():
        for convertible, value in convertibles.items():
            rates.append({
                'base_currency': base,
                'convertible_currency': convertible,
                'value': value
            })

    serializer = CurrencyRateSerializer(data=rates, many=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()


def convert(base_currency, convertible_currency, amount):
    rate_value = EQUAL_CODE_RATE_VALUE

    if not base_currency == convertible_currency:
        rate = CurrencyRate.objects.filter(
            base_currency=base_currency,
            convertible_currency=convertible_currency
        ).order_by('-created_at').first()

        if not rate:
            return None

        rate_value = rate.value

    converted_amount = Decimal(amount * rate_value).quantize(Decimal('1.00'))

    return float(converted_amount)
