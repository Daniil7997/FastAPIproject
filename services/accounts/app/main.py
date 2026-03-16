from fastapi import FastAPI

from app.api.v1.routers import main_router


application = FastAPI()

application.include_router(main_router)
