import pytest
from mimesis import Internet, Numeric
from pydantic import BaseModel

from server.apps.identity.models import User
from server.apps.pictures.models import FavouritePicture


class PictureData(BaseModel):
    """Dataclass for picture data."""

    foreign_id: int
    url: str


@pytest.fixture()
def picture_data() -> PictureData:
    """Factory for PictureData."""
    return PictureData(
        foreign_id=Numeric().increment(),
        url=Internet().url(),
    )


@pytest.fixture()
def favourite_picture_factory(picture_data: PictureData) -> FavouritePicture:
    """Favourite picture factory."""
    def create_favourite_picture(  # noqa: WPS430
        user: User,
    ) -> FavouritePicture:
        """Create a favourite picture."""
        return FavouritePicture.objects.create(
            user=user,
            foreign_id=picture_data.foreign_id,
            url=picture_data.url,
        )
    return create_favourite_picture
