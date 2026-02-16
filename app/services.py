from datetime import datetime
import asyncio
import httpx

from fastapi import HTTPException

import aiosqlite

from app.dependancy import get_db

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
    try:
        await db.execute(
            """
            INSERT INTO cities (city, latitude, longitude)
            VALUES (?, ?, ?)
            """,
            (city, lat, lon)
        )
        await db.commit()
    except(aiosqlite.IntegrityError):
        raise HTTPException(403, "Город уже добавлен")


async def save_current_wether_every_15_min(city: str, lat: float, lon: float) -> dict:
    """Запрос погоды: температура, влажность, скорость ветра, осадки"""

    while True:
        db = get_db()
        
        weather = await fetch_current_weather_by_coords(lat, lon)

        result = {
            "city": city,
            "time": weather["current"]["time"].split("T")[1],
            "temperature": weather["current"]["temperature_2m"],
            "humidity": weather["current"]["relative_humidity_2m"],
            "wind_speed": weather["current"]["wind_speed_10m"],
            "precipitation": weather["current"]["precipitation"],
        }
        await asyncio.sleep(900.0)





