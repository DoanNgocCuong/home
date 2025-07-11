import logging
import tracemalloc
from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.routers.api import api_router
from src.services.rag import Rag
from src.settings import APP_CONFIGS, SETTINGS

tracemalloc.start()


# Define the filter
class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return (
            record.args is not None
            and len(record.args) >= 3
            and list(record.args)[2] not in ["/health", "/ready"]
        )


logging.getLogger("uvicorn.access").addFilter(EndpointFilter())


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.rag_service = Rag()
    yield


app = FastAPI(**APP_CONFIGS, lifespan=lifespan)


@app.get("/health", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ready", include_in_schema=False)
async def readycheck() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(
    api_router,
    prefix=SETTINGS.API_V1_STR,
)
