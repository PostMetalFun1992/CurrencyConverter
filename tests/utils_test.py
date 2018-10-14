import pytest
from rest_framework import serializers, status

from converter_app.models import CurrencyRate
from converter_app import utils


R = CurrencyRate.objects.create


def rates_count(rates):
    return sum([
        len(rates[base]) for base in rates
    ])


class TestGetCurrencyRates:
    @pytest.mark.parametrize('base,convertibles,status,json,result', [
        (
            'USD',
            {'EUR', 'CZK'},
            status.HTTP_200_OK,
            {
                'rates': {
                    'EUR': 0.8745080892,
                    'CZK': 22.5666812418,
                    'PLN': 3.7739396589,
                }
            },
            {
                'EUR': 0.8745080892,
                'CZK': 22.5666812418,
            }
        ),
        (
            'USD',
            {'EUR', 'CZK', 'PLN'},
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            None,
            {}
        )
    ])
    def test_get_currency_rates(
        self, rates_api_response, base, convertibles, status, json, result
    ):
        rates_api_response(status, json)

        assert utils._get_currency_rate(base, convertibles) == result


class TestLoadRates:
    @pytest.mark.parametrize('rates', [
        {'USD': {}, 'EUR': {}},
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
            'USD': {
                'EUR': 0.8745080892,
                'CZK': 22.5666812418,
                'PLN': 3.7739396589
            }
        },
    ])
    def test_load_rates_with_existing(self, monkeypatch, rates):
        monkeypatch.setattr(utils, 'get_currencies_rates', lambda: rates)

        R(base_currency='USD', convertible_currency='EUR', value=0.8639308855)
        rates_count_before = CurrencyRate.objects.count()

        utils.load_rates()

        assert CurrencyRate.objects.count() == \
            rates_count_before + rates_count(rates)

    def test_prevent_load_rates_with_equal_code(self, monkeypatch):
        rates = {'USD': {'USD': 1.0}, 'EUR': {'USD': 1.1575}}
        monkeypatch.setattr(utils, 'get_currencies_rates', lambda: rates)

        R(base_currency='USD', convertible_currency='EUR', value=0.8639308855)
        rates_count_before = CurrencyRate.objects.count()

        with pytest.raises(serializers.ValidationError) as excinfo:
            utils.load_rates()

        assert 'Base currency code cannot equal to convertible' in \
            str(excinfo.value)
        assert CurrencyRate.objects.count() == rates_count_before


class TestConvertAmount:
    @pytest.mark.parametrize('base,convertible,value,amount,result', [
        ('USD', 'CZK', 22.5666812418, 5.0, 112.83),
        ('USD', 'CZK', 22.5666812418, 5.5, 124.12),
        ('USD', 'CZK', 22.5666812418, 0.5, 11.28),
        ('USD', 'EUR', 0.8745080892, 5.0, 4.37),
        ('USD', 'EUR', 0.8745080892, 5.5, 4.81),
        ('USD', 'EUR', 0.8745080892, 0.5, 0.44),
        ('USD', 'USD', 1.5, 5.0, 5.0),
        ('USD', 'USD', 1.5, 5.5, 5.5),
        ('USD', 'USD', 1.5, 0.5, 0.5),
        ('USD', 'EUR', 0.8745080892, 0.0, 0.0),
    ])
    def test_convert_amount(self, base, convertible, value, amount, result):
        R(base_currency=base, convertible_currency=convertible, value=value)

        assert utils.convert_amount(base, convertible, amount) == result

    def test_return_none_when_rates_not_found(self):
        base, convertible_1, convertible_2 = 'USD', 'CZK', 'EUR'
        value_1, amount = 22.5666812418, 5.0

        R(
            base_currency=base,
            convertible_currency=convertible_1,
            value=value_1
        )

        assert utils.convert_amount(base, convertible_2, amount) is None
