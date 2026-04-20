from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.v1.routers import main_router
from app.core.config import settings


application = FastAPI(root_path=settings.api_root_url)

application.include_router(main_router)

Instrumentator().instrument(application).expose(application,
                                                include_in_schema=False)
