from contextlib import asynccontextmanager

from fastapi import FastAPI
from redis.asyncio import Redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.v1.routers import main_router
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client = Redis.from_url(settings.url_redis)
    FastAPICache.init(RedisBackend(redis_client))
    yield
    await redis_client.aclose()


application = FastAPI(root_path=settings.api_root_url,
                      lifespan=lifespan)

application.include_router(main_router)

Instrumentator().instrument(application).expose(application,
                                                include_in_schema=False)
