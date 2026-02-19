from pydantic import BaseModel


class CurrentResponse(BaseModel):
    temperature: float
    wind_speed: float
    atmospheric_pressure: float


class CityCreate(BaseModel):
    city: str
    lat: float
    lon: float


class CitiesResponse(BaseModel):
    cities: list[str] | None



class CityResponse(BaseModel):
    city: str
    time: str
    temperature: float | None = None
    humidity: float | None = None
    wind_speed: float | None = None
    precipitation: float | None = None