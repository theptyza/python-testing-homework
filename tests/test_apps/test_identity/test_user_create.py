from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User


@pytest.mark.django_db()
def test_user_create(
    client: Client,
    test_email: str,
    test_password: str,
    user_data_factory,
    assert_user_data,
):
    """Create a new user."""
    user_data = user_data_factory()
    response = client.post(
        reverse('identity:registration'),
        data={
            'email': test_email,
            'password1': test_password,
            'password2': test_password,
            **user_data,
        },
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == reverse('identity:login')

    user = User.objects.get(email=test_email)
    assert user.id
    assert_user_data(user, user_data)


@pytest.mark.django_db()
@pytest.mark.parametrize(
    'required_field',
    [
        'email',
        'first_name',
        'last_name',
        'address',
        'job_title',
        'phone',
        'password1',
        'password2',
    ],
)
def test_user_required_fields(
    client: Client,
    test_email: str,
    test_password: str,
    user_data_factory,
    required_field: str,
):
    """Check that user can't be created without required fields."""
    registration_data = {
        'email': test_email,
        'password1': test_password,
        'password2': test_password,
        **user_data_factory(),
    }
    registration_data.pop(required_field)

    response = client.post(
        reverse('identity:registration'),
        data=registration_data,
    )

    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db()
def test_user_empty_dob(
    client: Client,
    test_email: str,
    test_password: str,
    user_data_factory,
):
    """Create a new user without date of birth."""
    user_data = user_data_factory()
    user_data.pop('date_of_birth')

    response = client.post(
        reverse('identity:registration'),
        data={
            'email': test_email,
            'password1': test_password,
            'password2': test_password,
            **user_data,
        },
    )

    assert response.status_code == HTTPStatus.FOUND
    assert response.url == reverse('identity:login')

    user = User.objects.get(email=test_email)
    assert user.date_of_birth is None


@pytest.mark.django_db()
def test_user_no_email():
    """Check that user can't be created without email."""
    with pytest.raises(
        ValueError,
        match='Users must have an email address',
    ):
        User.objects.create_user(  # noqa: S106
            email=None,
            password='testpassword',
        )
