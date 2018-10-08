import django
import pytest
from rest_framework.test import APIClient


@pytest.fixture(autouse=True)
def django_setup():
    django.setup()


@pytest.fixture(autouse=True)
def enable_db_access(db):
    pass


@pytest.fixture(autouse=True)
def api_client():
    return APIClient()
