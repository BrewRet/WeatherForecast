from datetime import date
import asyncio
import logging

from app.services import fetch_current_weather_by_coords
from app.config import get_settings

import aiosqlite


logger = logging.getLogger(__name__)

settings = get_settings()

async def save_current_wether_every_15_min() -> None:
    """Фоновая задача для получения погоды каждые 15 минут"""

    while True:
        async with aiosqlite.connect(settings.db_path) as db:
            try:

                date_now = date.today().isoformat()
                async with db.execute(
                    """
                    SELECT city, latitude, longitude, created_at FROM cities
                    """
                ) as cursor:
                    async for row in cursor:
                        if row != None:
                            city, lat, lon, created_at = row
                            if created_at[:10] != date_now:
                                continue

                            weather = await fetch_current_weather_by_coords(lat, lon)
                            await db.execute(
                                """
                                INSERT INTO weather (city, temperature, humidity, wind_speed, precipitation)
                                VALUES (?, ?, ?, ?, ?)
                                """,
                                (city, weather["current"]["temperature_2m"], weather["current"]["relative_humidity_2m"],
                                weather["current"]["wind_speed_10m"], weather["current"]["precipitation"])
                            )
                            await db.commit()
                await db.close()
            except Exception as e:
                logger.error(e)
        await asyncio.sleep(900)