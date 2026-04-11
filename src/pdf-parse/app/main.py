import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.exception_handlers import api_exception_handler
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
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register exception handlers
app.add_exception_handler(HTTPException, api_exception_handler)
app.add_exception_handler(RequestValidationError, api_exception_handler)
app.add_exception_handler(Exception, api_exception_handler)

# Register routes
app.include_router(extract.router)
app.include_router(health.router)
