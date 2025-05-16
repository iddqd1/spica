import pytest
from rest_framework.test import APIClient

from spica.users.models import User
from spica.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def _media_storage(settings, tmpdir) -> None:
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user(db) -> User:
    return UserFactory()


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def client_authenticated(user, client):
    client.force_authenticate(user=user)
    return client
