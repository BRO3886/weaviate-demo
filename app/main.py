from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import router
from app.core import close_services, init_services


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_services()
    yield
    await close_services()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(router)
    return app


app = create_app()
