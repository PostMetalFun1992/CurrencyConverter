import os

CURRENCIES = set(os.getenv('CURRENCIES', '').split(','))
RATES_API_URL = os.getenv('RATES_API_URL', '')
RATES_UPDATE_PERIOD_DAYS = int(os.getenv('RATES_UPDATE_PERIOD_DAYS', '1'))
