import pytest
from rest_framework import status

from converter_app.models import CurrencyRate


class TestConvertAmount:
    @pytest.mark.parametrize('base,convertible,value,amount,result', [
        ('USD', 'CZK', 22.5666812418, 5.0, 112.83),
        ('USD', 'CZK', 22.5666812418, 5.5, 124.12),
        ('USD', 'CZK', 22.5666812418, 0.5, 11.28),
        ('USD', 'EUR', 0.8745080892, 5.0, 4.37),
        ('USD', 'EUR', 0.8745080892, 5.5, 4.81),
        ('USD', 'EUR', 0.8745080892, 0.5, 0.44),
        ('USD', 'USD', 0.8745080892, 0.5, 0.5),
        ('USD', 'USD', 1.5, 5.0, 5.0),
        ('USD', 'USD', 1.5, 5.5, 5.5),
        ('USD', 'USD', 1.5, 0.5, 0.5),
    ])
    def test_convert_amount(
        self, api_client, base, convertible, value, amount, result
    ):
        CurrencyRate.objects.create(
            base_currency=base,
            convertible_currency=convertible,
            value=value
        )
        data = {
            'base_currency': base,
            'convertible_currency': convertible,
            'amount': amount
        }

        r = api_client.put('/conversation/', data=data, format='json')

        assert r.status_code == status.HTTP_200_OK

        assert r.data['base_currency'] == base
        assert r.data['convertible_currency'] == convertible
        assert r.data['amount'] == amount
        assert r.data['converted_amount'] == result

    def test_get_latest_rate(self, api_client):
        first_value, last_value, amount = 0.8, 0.9, 5.0

        CurrencyRate.objects.create(
            base_currency='USD',
            convertible_currency='EUR',
            value=first_value
        )

        CurrencyRate.objects.create(
            base_currency='USD',
            convertible_currency='EUR',
            value=last_value
        )

        data = {
            'base_currency': 'USD',
            'convertible_currency': 'EUR',
            'amount': amount
        }

        r = api_client.put('/conversation/', data=data, format='json')

        assert r.status_code == status.HTTP_200_OK
        assert r.data['converted_amount'] == last_value * amount

    @pytest.mark.parametrize('base,convertible,info', [
        ('USD', 'ZZZ', 'ZZZ'),
        ('ZZZ', 'USD', 'ZZZ'),
        ('ZZZ', 'ZZZ', 'ZZZ'),
    ])
    def test_400_when_not_supported_currencies(
        self, api_client, base, convertible, info
    ):
        data = {
            'base_currency': base,
            'convertible_currency': convertible,
            'amount': 5.0
        }

        r = api_client.put('/conversation/', data=data, format='json')

        assert r.status_code == status.HTTP_400_BAD_REQUEST
        for value in r.data.values():
            assert '"{}" is not a valid choice.'.format(info) in str(value)

    def test_404_when_not_found_rates(self, api_client):
        data = {
            'base_currency': 'USD',
            'convertible_currency': 'EUR',
            'amount': 5.0
        }

        r = api_client.put('/conversation/', data=data, format='json')

        assert r.status_code == status.HTTP_404_NOT_FOUND
        assert 'Cannot found rates: {}-{}'.format('USD', 'EUR') in r.data
