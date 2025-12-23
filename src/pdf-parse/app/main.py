from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import extract, health

app = FastAPI(
    title=settings.title,
    description=settings.description,
    version=settings.version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
)

app.include_router(extract.router)
app.include_router(health.router)
