from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.routes import router as prediction_router
from app.utils.logger import log


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    """
    log.info("OncoVision API started successfully")
    yield
    log.info("OncoVision API shutting down")


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.
    """
    app = FastAPI(
        title="OncoVision API",
        description="CNN-based medical image analysis backend",
        version="1.0.0",
        lifespan=lifespan
    )

    app.include_router(
        prediction_router,
        prefix="",
        tags=["Cancer Detection"]
    )

    return app


app = create_app()
