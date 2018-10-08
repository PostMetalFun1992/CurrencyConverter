import os

import requests as r
from rest_framework import status


OEX_RATES_URL = 'https://openexchangerates.org/api/latest.json'
OEX_APP_ID = os.getenv('OEX_APP_ID', '')
CURRENCIES = set(os.getenv('CURRENCIES', '').split(','))  # TODO: prevent typos

# TODO: caclulate all rates with one request


def get_currency_combos():
    return {curr: CURRENCIES - {curr} for curr in CURRENCIES}


def get_currency_rate(base_currency, converted_currencies):
    resp = r.get(
        OEX_RATES_URL,
        params={'app_id': OEX_APP_ID, 'base': base_currency}
    )

    if not resp.status_code == status.HTTP_200_OK:
        return {}

    rates = resp.json()['rates']

    return {curr: rates[curr] for curr in converted_currencies}
