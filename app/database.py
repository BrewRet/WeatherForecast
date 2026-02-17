import aiosqlite

from app.config import get_settings


settings = get_settings()

async def init_db():
    async with aiosqlite.connect(settings.db_path) as db:
        await db.execute("PRAGMA foreign_keys = ON")
        await db.execute("PRAGMA journal_mode = WAL")
        await db.execute("""
            CREATE TABLE IF NOT EXISTS cities (
                city TEXT NOT NULL UNIQUE,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS weather (
                city TEXT,
                time TEXT,
                temperature REAL,
                humidity REAL,
                wind_speed REAL,
                precipitation REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (city) REFERENCES cities(city) ON DELETE CASCADE
            )
        """)
        await db.commit()
