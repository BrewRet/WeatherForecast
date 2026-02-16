from datetime import datetime, date
import asyncio
import httpx

import aiosqlite

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
HTTP_TIMEOUT = 10.0
CURRENT_WEATHER_PARAMS="temperature_2m,wind_speed_10m,surface_pressure,precipitation,relative_humidity_2m"


async def fetch_current_weather_by_coords(lat: float, lon: float) -> dict:
    """Получить погоду по координатам"""

    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        response = await client.get(
            OPEN_METEO_URL,
            params={
                "latitude": lat,
                "longitude": lon,
                "wind_speed_unit": "ms",
                "current": CURRENT_WEATHER_PARAMS,
            },
        )
        response.raise_for_status()

        return response.json()


async def get_current_weather_to_show(lat: float, lon: float) -> dict:
    """Запрос погоды: температура, скорость ветра, атмосферное давление"""

    weather = await fetch_current_weather_by_coords(lat, lon)

    return {
        "current": {
            "temperature": weather["current"]["temperature_2m"],
            "wind_speed": weather["current"]["wind_speed_10m"],
            "atmospheric_pressure": weather["current"]["surface_pressure"],
        }
    }


async def add_city_to_db(city: str, lat: float, lon: float, db: aiosqlite.Connection):
    """Добавление города в базу данных"""

    await db.execute(
        """
        INSERT INTO cities (city, latitude, longitude)
        VALUES (?, ?, ?)
        """,
        (city, lat, lon)
    )
   


async def get_list_of_cities(db:aiosqlite.Connection) -> list[str]:
    """Выдача городов из базы данных"""

    cursor = await db.execute(
        """
        SELECT city FROM cities 
        """
    )
    cities = await cursor.fetchall()
    result = []
    for city in cities:
        city = ''.join(city)
        result.append(city)
    return result





async def get_weather_from_db_by_city_time(city: str, time: str) -> dict:
    """"""
    
    pass




