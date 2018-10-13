from decimal import Decimal

from django.http import Http404
from rest_framework import serializers, status
import requests as r

from converter.enviroments import CURRENCIES, RATES_API_URL
from converter_app.models import CurrencyRate
from converter_app.serializers import CurrencyRateSerializer


def _calc_combos(currencies_set=CURRENCIES):
    return {c: currencies_set - {c} for c in currencies_set}


def _get_currency_rate(base, convertibles):
    resp = r.get(RATES_API_URL, params={'base': base})

    if not resp.status_code == status.HTTP_200_OK:
        return {}

    rates = resp.json()['rates']

    return {currency: rates[currency] for currency in convertibles}


def get_currencies_rates():
    return {base: _get_currency_rate(base, convertibles)
            for base, convertibles in _calc_combos().items()}


def load_rates():
    pair_rates = []
    for base, convertibles in get_currencies_rates().items():
        for convertible, value in convertibles.items():
            pair_rates.append({
                'base_currency': base,
                'convertible_currency': convertible,
                'value': value
            })

    serializer = CurrencyRateSerializer(data=pair_rates, many=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()


def convert_amount(base_currency, convertible_currency, amount):
    rate_value = 1.0

    if not base_currency == convertible_currency:
        rate = CurrencyRate.objects.filter(
            base_currency=base_currency,
            convertible_currency=convertible_currency
        ).order_by('created_at').first()

        if not rate:
            return None

        rate_value = rate.value

    converted_amount = Decimal(amount * rate_value).quantize(Decimal('1.00'))

    return float(converted_amount)
