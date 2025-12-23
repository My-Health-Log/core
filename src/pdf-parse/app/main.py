import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import extract, health
from app.services.provider import get_provider


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load docling
    logger = logging.getLogger("uvicorn")
    logger.propagate = False
    app.state.logger = logger
    logger.info("Loading startup dependencies")
    logger.info("1) Loading docling...")
    app.state.provider = get_provider()
    logger.info("✅ Docling...")
    logger.info("✅ Finished loading startup dependencies")
    yield
    logger.info("Cleanup dependencies")
    # add on app exit logic here


app = FastAPI(
    title=settings.title,
    description=settings.description,
    version=settings.version,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
)

app.include_router(extract.router)
app.include_router(health.router)
