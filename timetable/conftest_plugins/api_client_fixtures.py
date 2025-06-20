from collections.abc import Callable

import pytest
from django.test import Client
from rest_framework.test import APIClient

from timetable.users.models import User


@pytest.fixture
def create_api_client() -> Callable[[], APIClient]:
    def _create_api_client(user: User | None = None) -> APIClient:
        client = APIClient()
        if user:
            client.force_authenticate(user)
        client.user = user  # type: ignore[attr-defined]
        return client

    return _create_api_client


@pytest.fixture
def unauthorized_api_client(create_api_client) -> APIClient:
    return create_api_client()


@pytest.fixture
def user_api_client(create_api_client, user) -> APIClient:
    return create_api_client(user)


@pytest.fixture
def admin_client(admin_user) -> Client:
    client = Client()
    client.force_login(admin_user)
    return client
