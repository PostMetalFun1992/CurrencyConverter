import pytest

from converter_app.models import CurrencyRate
from converter_app.utils import convert_amount


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

        assert convert_amount(base, convertible, amount) == result
