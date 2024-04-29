from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse

from server.apps.identity.models import User
from server.apps.pictures.logic.usecases.favourites_list import FavouritesList
from tests.plugins.pictures.pictures import PictureData


@pytest.mark.django_db()
def test_add_picture(
    test_user: User,
    auth_client: Client,
    picture_data: 'PictureData',
):
    """Add a picture to favourites."""
    response = auth_client.get(reverse('pictures:dashboard'))
    assert response.status_code == HTTPStatus.OK

    auth_client.post(
        reverse('pictures:dashboard'),
        data=picture_data.dict(),
    )
    assert response.status_code == HTTPStatus.OK

    favourite_pictures = FavouritesList()(test_user.id).all()
    assert len(favourite_pictures) == 1
    assert favourite_pictures[0].foreign_id == picture_data.foreign_id
    assert favourite_pictures[0].url == picture_data.url


@pytest.mark.django_db()
def test_get_pictures(
    test_user: User,
    auth_client: Client,
    favourite_picture_factory,
):
    """Get favourite pictures."""
    favourite_picture = favourite_picture_factory(test_user)

    response = auth_client.get(reverse('pictures:favourites'))

    assert response.status_code == HTTPStatus.OK
    assert favourite_picture.url in response.content.decode()
