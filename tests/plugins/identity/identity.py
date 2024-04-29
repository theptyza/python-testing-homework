import pytest
from mimesis import Address, Datetime, Person

from server.apps.identity.models import User


@pytest.fixture()
def test_email() -> str:
    """Test email."""
    return Person().email()


@pytest.fixture()
def test_password() -> str:
    """Test password."""
    return 'testpassword'


@pytest.fixture()
def user_data_factory():
    """Registration data."""
    def generate_user_data() -> dict:  # noqa: WPS430
        person = Person()

        return {
            'first_name': person.first_name(),
            'last_name': person.last_name(),
            'date_of_birth': Datetime().formatted_date(
                fmt='%Y-%m-%d',  # noqa: WPS323
            ),
            'address': Address().address(),
            'job_title': person.occupation(),
            'phone': person.phone_number(),
        }
    return generate_user_data


@pytest.fixture()
def test_user(
    test_email: str,
    test_password: str,
    user_data_factory,
) -> User:
    """User with test email."""
    return User.objects.create_user(
        test_email,
        test_password,
        **user_data_factory(),
    )
