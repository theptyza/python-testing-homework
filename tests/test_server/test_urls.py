from http import HTTPStatus

import pytest
from django.test import Client


@pytest.mark.django_db()
def test_health_check(client: Client) -> None:
    """This test ensures that health check is accessible."""
    response = client.get('/health/')

    assert response.status_code == HTTPStatus.OK


def test_admin_unauthorized(client: Client) -> None:
    """This test ensures that admin panel requires auth."""
    response = client.get('/admin/')

    assert response.status_code == HTTPStatus.FOUND


@pytest.mark.django_db()
def test_admin_authorized(admin_client: Client) -> None:
    """This test ensures that admin panel is accessible."""
    response = admin_client.get('/admin/')

    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db()
@pytest.mark.parametrize('page', [
    '/pictures/dashboard',
    '/pictures/favourites',
    '/identity/update',
])
def test_page_unauthorized(client: Client, page: str) -> None:
    """This test ensures that pages requires auth."""
    response = client.get(page)

    assert response.status_code == HTTPStatus.FOUND


@pytest.mark.django_db()
@pytest.mark.parametrize('page', [
    '/pictures/dashboard',
    '/pictures/favourites',
    '/identity/update',
])
def test_pictures_dashboard_authorized(auth_client: Client, page: str) -> None:
    """This test ensures that pages are accessible with auth."""
    response = auth_client.get(page)

    assert response.status_code == HTTPStatus.OK


def test_admin_docs_unauthorized(client: Client) -> None:
    """This test ensures that admin panel docs requires auth."""
    response = client.get('/admin/doc/')

    assert response.status_code == HTTPStatus.FOUND


@pytest.mark.django_db()
def test_admin_docs_authorized(admin_client: Client) -> None:
    """This test ensures that admin panel docs are accessible."""
    response = admin_client.get('/admin/doc/')

    assert response.status_code == HTTPStatus.OK
    assert b'docutils' not in response.content


@pytest.mark.django_db()
def test_home_page(client: Client) -> None:
    """This test ensures that home page is accessible."""
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize('page', [
    '/robots.txt',
    '/humans.txt',
])
def test_specials_txt(client: Client, page: str) -> None:
    """This test ensures that special `txt` files are accessible."""
    response = client.get(page)

    assert response.status_code == HTTPStatus.OK
    assert response.get('Content-Type') == 'text/plain'
