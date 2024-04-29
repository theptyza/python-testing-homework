from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User


@pytest.mark.django_db()
def test_user_login(
    client: Client,
    test_user: User,
    test_password: str,
):
    """Login with existing user."""
    response = client.post(
        reverse('identity:login'),
        {
            'username': test_user.email,
            'password': test_password,
        },
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == reverse('pictures:dashboard')


@pytest.mark.django_db()
def test_user_login_invalid_password(
    client,
    test_user,
):
    """Login with invalid password."""
    response = client.post(
        reverse('identity:login'),
        {
            'username': test_user.email,
            'password': 'WRONGPASSWORD',
        },
    )

    assert response.status_code == HTTPStatus.OK
