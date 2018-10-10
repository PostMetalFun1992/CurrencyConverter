import django
import pytest
import requests
from rest_framework.test import APIClient


@pytest.fixture(autouse=True)
def django_setup():
    django.setup()


@pytest.fixture(autouse=True)
def enable_db_access(db):
    pass


@pytest.fixture()
def api_client():
    return APIClient()


@pytest.fixture()
def rates_api_response(monkeypatch):
    class DummyResponse:
        pass

    response = DummyResponse()

    def _rates_api_get_response(status, json):
        setattr(response, 'status_code', status)
        setattr(response, 'json', lambda: json)

        monkeypatch.setattr(requests, 'get', lambda url, params: response)

    return _rates_api_get_response
