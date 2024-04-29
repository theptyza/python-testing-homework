from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User


@pytest.mark.django_db()
def test_user_update(
    auth_client: Client,
    test_user: User,
    user_data_factory,
    assert_user_data,
):
    """Update user data."""
    update_data = user_data_factory()

    response = auth_client.post(
        reverse('identity:user_update'),
        data=update_data,
        follow=True,
    )
    assert response.status_code == HTTPStatus.OK

    user = User.objects.get(email=test_user.email)
    assert user.id
    assert_user_data(user, update_data)
