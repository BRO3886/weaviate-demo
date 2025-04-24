import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api import router
from app.api.middleware import GlobalExceptionMiddleware, StaticFilesHandler
from app.services import close_services, init_services


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_services()
    yield
    await close_services()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "HEAD"],
        allow_headers=["*"],
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],  # Vite dev server default port
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    static_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static"
    )
    if os.path.exists(static_dir):
        app.mount("/static", StaticFilesHandler(directory=static_dir), name="static")

    app.include_router(router)
    app.add_middleware(GlobalExceptionMiddleware)
    return app


app = create_app()
