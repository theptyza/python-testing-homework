"""
This module is used to provide configuration, fixtures, and plugins for pytest.

It may be also used for extending doctest's context:
1. https://docs.python.org/3/library/doctest.html
2. https://docs.pytest.org/en/latest/doctest.html
"""

from datetime import datetime

import pytest
from django.test import Client

from server.apps.identity.models import User


@pytest.fixture()
def auth_client(
    client: Client,
    test_user: User,
) -> Client:
    """Authenticated client."""
    client.force_login(test_user)
    return client


@pytest.fixture(scope='session')
def assert_user_data():
    """Assert user data."""
    def _assert_user_data(user: User, user_data: dict):  # noqa: WPS430
        assert user.first_name == user_data['first_name']
        assert user.last_name == user_data['last_name']
        assert user.address == user_data['address']
        assert (
            user.date_of_birth == datetime.strptime(
                user_data['date_of_birth'],
                '%Y-%m-%d',
            ).date()
        )
        assert user.job_title == user_data['job_title']
        assert user.phone == user_data['phone']
    return _assert_user_data


pytest_plugins = [
    # Should be the first custom one:
    'tests.plugins.django_settings',
    # TODO: add your own plugins here!
    'tests.plugins.identity.identity',
    'tests.plugins.pictures.pictures',
]
