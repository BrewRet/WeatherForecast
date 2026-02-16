from fastapi import APIRouter, status, Depends, HTTPException

import aiosqlite

from app.dependancy import get_db
from app.schemas import (
    CurrentResponse,
    CityRequestParams,
    CitiesResponse,
    CityCreate,
    CityResponse,
)
from app.services import (
    get_current_weather_to_show,
    add_city_to_db,
)

router = APIRouter(
    prefix="/weather",
    tags=["weather"],
)


@router.get(
        "/current", 
        response_model=CurrentResponse,
        status_code=status.HTTP_200_OK,
        summary="Получить погоду по координатам",
)
async def get_current_weather(lat: float, lon: float) -> CurrentResponse:
    """
    Получить погоду в момент запроса.
    
    - **lat**: долгота
    - **lon**: широта
    """
    data = await get_current_weather_to_show(lat, lon)
    return CurrentResponse(
        temperature=data["temperature"],
        wind_speed=data["wind_speed"],
        atmospheric_pressure=data["atmospheric_pressure"],
    )


@router.post(
        "/cities",
        
)
async def add_city_with_coords(
    request: CityCreate,
    db: aiosqlite.Connection = Depends(get_db)) -> None:
    """Добавить город в список городов для мониторинга погоды"""
    
    return await add_city_to_db(request.city, request.lat, request.lon, db)
    


@router.get(
        "/cities",
        response_model=CitiesResponse,
)
async def get_cities_with_weather_forecast(db: aiosqlite.Connection = Depends(get_db)) -> CitiesResponse:


    pass


@router.get(
        "/cities/{city}/{time}",
        response_model=CityResponse
)
async def get_weather_from_city_at_time(
    city: str,
    time: str, 
    params: CityRequestParams,
    db: aiosqlite.Connection = Depends(get_db),
    ) -> CityResponse:


    pass