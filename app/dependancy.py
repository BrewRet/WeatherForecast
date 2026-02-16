import aiosqlite
from app.config import get_settings


settings = get_settings()

async def get_db():
    async with aiosqlite.connect(settings.db_path) as db:
        try:
            yield db
        finally:
            db.close()