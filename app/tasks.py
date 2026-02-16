from datetime import date
import asyncio

from app.services import fetch_current_weather_by_coords
from app.config import get_settings

import aiosqlite


settings = get_settings()

async def save_current_wether_every_15_min() -> None:
    """Фоновая задача для получения погоды каждые 15 минут"""

    while True:
        async with aiosqlite.connect(settings.db_path) as db:

            date_now = date.today().isoformat()
            cursor = await db.execute(
                """
                SELECT * FROM cities
                """
            )
            cities_data = await cursor.fetchall()
            for row in cities_data:
                city, lat, lon, created_at = row
                if created_at[:10] != date_now:
                    await db.execute(
                        """
                        DELETE FROM cities WHERE created_at == ?
                        """,
                        (created_at,)
                    )
                    db.commit()
                    continue

                weather = await fetch_current_weather_by_coords(lat, lon)
                await db.execute(
                    """
                    INSERT INTO WEATHER (city, temperature, himidity, wind_speed, preciptation)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (city, weather["current"]["temperature_2m"], weather["current"]["relative_humidity_2m"],
                    weather["current"]["wind_speed_10m"], weather["current"]["precipitation"])
                )
                
        await asyncio.sleep(900.0)