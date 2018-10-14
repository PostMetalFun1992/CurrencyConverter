import pytest
from rest_framework import status

from converter_app.models import CurrencyRate


R = CurrencyRate.objects.create


class TestCurrencyConversationView:
    def test_put(self, api_client):
        base, convertible = 'USD', 'CZK'
        value, amount, result = 22.5666812418, 5.0, 112.83

        R(base_currency=base, convertible_currency=convertible, value=value)

        r = api_client.put(
            '/conversation/',
            data={
                'base_currency': base,
                'convertible_currency': convertible,
                'amount': amount
            },
            format='json'
        )

        assert r.status_code == status.HTTP_200_OK

        assert r.data['base_currency'] == base
        assert r.data['convertible_currency'] == convertible
        assert r.data['amount'] == amount
        assert r.data['converted_amount'] == result

    def test_convert_with_latest_rate(self, api_client):
        base, convertible = 'USD', 'EUR'
        value_1, value_2, amount = 0.8, 0.9, 5.0

        R(base_currency=base, convertible_currency=convertible, value=value_1)
        R(base_currency=base, convertible_currency=convertible, value=value_2)

        r = api_client.put(
            '/conversation/',
            data={
                'base_currency': base,
                'convertible_currency': convertible,
                'amount': amount
            },
            format='json'
        )

        assert r.status_code == status.HTTP_200_OK
        assert r.data['converted_amount'] == value_2 * amount

    @pytest.mark.parametrize('base,convertible,info', [
        ('USD', 'ZZZ', 'ZZZ'),
        ('ZZZ', 'USD', 'ZZZ'),
        ('ZZZ', 'ZZZ', 'ZZZ'),
    ])
    def test_400_when_not_supported_currencies(
        self, api_client, base, convertible, info
    ):
        r = api_client.put(
            '/conversation/',
            data={
                'base_currency': base,
                'convertible_currency': convertible,
                'amount': 0.0
            },
            format='json'
        )

        assert r.status_code == status.HTTP_400_BAD_REQUEST
        for value in r.data.values():
            assert '"{}" is not a valid choice.'.format(info) in str(value)

    def test_404_when_not_found_rates(self, api_client):
        base, convertible = 'USD', 'EUR'

        r = api_client.put(
            '/conversation/',
            data={
                'base_currency': base,
                'convertible_currency': convertible,
                'amount': 0.0
            },
            format='json'
        )

        assert r.status_code == status.HTTP_404_NOT_FOUND
        assert 'Cannot found rates: {}-{}'.format(base, convertible) in r.data

    def test_400_when_amount_is_negative(self, api_client):
        base, convertible = 'USD', 'EUR'
        value, amount = 0.8, -1.0

        R(base_currency=base, convertible_currency=convertible, value=value)

        r = api_client.put(
            '/conversation/',
            data={
                'base_currency': base,
                'convertible_currency': convertible,
                'amount': amount
            },
            format='json'
        )

        assert r.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Ensure this value is greater than or equal to 0.' in \
            r.data['amount']
