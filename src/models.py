from pydantic import BaseModel
from datetime import datetime


class HouseModel(BaseModel):
    advert_type: str
    utc_created_at: datetime
    province: str | None = None
    subregion: str | None = None
    location: str | None = None
    market: str | None = None
    lot_area: int | float
    house_area: int | float
    n_rooms: int | None
    build_year: int


class ApartmentModel(BaseModel):
    advert_type: str
    utc_created_at: datetime
    province: str | None = None
    subregion: str | None = None
    market: str | None = None
    apartment_area: int | float
    n_rooms: int | None
    build_year: int


class LandModel(BaseModel):
    advert_type: str
    utc_created_at: datetime
    province: str | None = None
    subregion: str | None = None
    location: str | None = None
    land_area: int | float
