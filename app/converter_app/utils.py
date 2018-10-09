import os

import requests as r
from rest_framework import status

from converter_app.serializers import CurrencyRateSerializer

RATES_API_URL = 'https://api.exchangeratesapi.io/latest'
CURRENCIES = set(os.getenv('CURRENCIES', '').split(','))


def _calc_combos():
    return {currency: CURRENCIES - {currency} for currency in CURRENCIES}


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
