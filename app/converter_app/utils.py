import os

import requests as r

OEX_RATES_URL = 'https://openexchangerates.org/api/latest.json'
OEX_APP_ID = os.getenv('OEX_APP_ID', '')


def get_currency_rate():
    response = r.get(
        OEX_RATES_URL,
        params={'app_id': OEX_APP_ID}
    )

    print(response.json())
