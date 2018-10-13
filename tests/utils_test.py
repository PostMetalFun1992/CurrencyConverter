from datetime import timedelta as td

from django.utils import timezone as tz
import pytest
from rest_framework import status as s, serializers

from converter.enviroments import RATES_UPDATE_PERIOD_DAYS
from converter_app.models import CurrencyRate
from converter_app import utils


def rates_count(rates):
    return sum([len(rates[k]) for k in rates])


class TestGetCurrencyRate:
    @pytest.mark.parametrize('status,json', [
        (
            s.HTTP_200_OK,
            {'rates': {
                'EUR': 0.8745080892,
                'CZK': 22.5666812418,
                'PLN': 3.7739396589,
            }}
        ),
        (
            s.HTTP_400_BAD_REQUEST,
            {'rates': {}},
        )
    ])
    def test_get_currency_rate(self, status, json, rates_api_response):
        rates_api_response(status, json)

        assert utils._get_currency_rate('USD', {
            'EUR', 'CZK', 'PLN'
        }) == json['rates']


class TestLoadRates:
    @pytest.mark.parametrize('rates', [
        {},
        {
            'USD': {
                'EUR': 0.8745080892,
                'CZK': 22.5666812418,
                'PLN': 3.7739396589
            }
        },
        {
            'USD': {'EUR': 0.8639308855},
            'EUR': {'USD': 1.1575},
        }
    ])
    def test_load_rates(self, monkeypatch, rates):
        monkeypatch.setattr(utils, 'get_currencies_rates', lambda: rates)

        utils.load_rates()

        assert CurrencyRate.objects.count() == rates_count(rates)

    @pytest.mark.parametrize('rates', [
        {'USD': {'EUR': 0.8639308855}},
        {
            'EUR': {'USD': 1.1575},
            'USD': {'EUR': 0.8639308855},
        },
    ])
    def test_load_rates_with_existing(self, monkeypatch, rates):
        rate = CurrencyRate.objects.create(
            base_currency='USD',
            convertible_currency='EUR',
            value=0.8639308855,
        )
        rate.created_at = tz.now() - td(days=RATES_UPDATE_PERIOD_DAYS)
        rate.save()

        rates_before = CurrencyRate.objects.count()
        monkeypatch.setattr(utils, 'get_currencies_rates', lambda: rates)

        utils.load_rates()

        assert CurrencyRate.objects.count() == \
            rates_before + rates_count(rates)

    @pytest.mark.parametrize('rates', [
        {
            'USD': {'USD': 1.0},
            'EUR': {'USD': 1.1575},
        }
    ])
    def test_load_rates_prevent_equal(self, monkeypatch, rates):
        CurrencyRate.objects.create(
            base_currency='USD',
            convertible_currency='EUR',
            value=0.8639308855,
        )
        rates_before = CurrencyRate.objects.count()
        monkeypatch.setattr(utils, 'get_currencies_rates', lambda: rates)

        with pytest.raises(serializers.ValidationError) as excinfo:
            utils.load_rates()

        assert 'Base currency code cannot equal to convertible' in \
            str(excinfo.value)
        assert CurrencyRate.objects.count() == rates_before


class TestConvertAmount:
    @pytest.mark.parametrize('base,convertible,value,amount,result', [
        ('USD', 'CZK', 22.5666812418, 5.0, 112.83),
        ('USD', 'CZK', 22.5666812418, 5.5, 124.12),
        ('USD', 'CZK', 22.5666812418, 0.5, 11.28),
        ('USD', 'EUR', 0.8745080892, 5.0, 4.37),
        ('USD', 'EUR', 0.8745080892, 5.5, 4.81),
        ('USD', 'EUR', 0.8745080892, 0.5, 0.44),
    ])
    def test_convert_amount(self, base, convertible, value, amount, result):
        CurrencyRate.objects.create(
            base_currency=base,
            convertible_currency=convertible,
            value=value
        )

        assert utils.convert_amount(base, convertible, amount) == result

    def test_none_when_not_found_rates(self):
        CurrencyRate.objects.create(
            base_currency='USD',
            convertible_currency='EUR',
            value=0.8639308855,
        )

        assert utils.convert_amount('USD', 'CZK', 50.0) is None
