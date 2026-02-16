import logging

import asyncio

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import get_settings
from app.routers import router as weather_router
from app.database import init_db


settings = get_settings()

logging.basicConfig(
    level=getattr(logging, "INFO", logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)
logger.info(
    f"Starting {settings.app_name} v{settings.version} on {settings.host}:{settings.port}"
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title=settings.app_name,
    description="""
## Тестовое задание для Инфотекс

# Сервис получения погоды

### Возможности:

- Получение погоды в данный момент по координатам
- Сохранение города в список городов
- Получения списка городов
- Получение погоды в городе из списка в заданое время
    """,
    version=settings.version,
    debug=settings.debug,
    lifespan=lifespan
)

app.include_router(weather_router)