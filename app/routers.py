from fastapi import APIRouter, status, Depends, HTTPException, Query

import aiosqlite
import logging  

from app.dependancy import get_db
from app.schemas import (
    CurrentResponse,
    CitiesResponse,
    CityCreate,
    CityResponse,
)
from app.services import (
    get_current_weather_to_show,
    add_city_to_db,
    get_list_of_cities,
    get_weather_from_db_by_city_time,
)

logger = logging.getLogger(__name__)

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
    return CurrentResponse(**data)


@router.post(
        "/cities",
        status_code=status.HTTP_201_CREATED,
        summary="Добавить город и его координаты в базу данных"
)
async def add_city_with_coords(
    request: CityCreate,
    db: aiosqlite.Connection = Depends(get_db)) -> None:
    """Добавить город в список городов для мониторинга погоды"""
    try:
        await add_city_to_db(request.city, request.lat, request.lon, db)
        return {"result": "Город успешно добавлен"}
    except(aiosqlite.IntegrityError):
        raise HTTPException(403, "Город уже добавлен")
    
    


@router.get(
        "/cities",
        response_model=CitiesResponse,
        status_code=status.HTTP_200_OK,
        summary="Получить список городов, для которых доступен прогноз"
)
async def get_cities_with_weather_forecast(db: aiosqlite.Connection = Depends(get_db)) -> CitiesResponse:
    cities = await get_list_of_cities(db)
    return CitiesResponse(cities=cities) 

    


@router.get(
        "/city",
        response_model=CityResponse,
        status_code=status.HTTP_200_OK,
        summary="Получить погоду по городу и времени"
)
async def get_weather_from_city_at_time(
    city: str,
    time: str,
    temperature: bool = Query(False, description="Включить температуру"),
    humidity: bool = Query(False, description="Включить влажность"),
    wind_speed: bool = Query(False, description="Включить скорость ветра"),
    precipitation: bool = Query(False, description="Включить осадки"),
    db: aiosqlite.Connection = Depends(get_db),
    ) -> CityResponse:

    params = {
        "temperature": temperature,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "precipitation": precipitation,
    }
    
    result = await get_weather_from_db_by_city_time(city, time, params, db)
    if not result:
        raise HTTPException(404, "Не найдена погода в заданом городе по заданному времени")
    return CityResponse(**result)
    
    