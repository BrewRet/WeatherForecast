import logging

import asyncio

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import get_settings
from app.routers import router as weather_router
from app.database import init_db
from app.tasks import save_current_wether_every_15_min


settings = get_settings()

logging.basicConfig(
    level=getattr(logging, "INFO", logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)
logger.info(
    f"Запуск {settings.app_name} v{settings.version} на {settings.host}:{settings.port}"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    try:
        task = asyncio.create_task(save_current_wether_every_15_min())
        yield
    except Exception as e:
        logger.error(f"Ошибка инициализации планировщика: {e}")
    finally:
        task.cancel()
        logger.info("Обновление погоды остановлено")



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
    lifespan=lifespan,
)

app.include_router(weather_router)