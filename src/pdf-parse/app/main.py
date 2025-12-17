from fastapi import FastAPI
from app.routers import extract, health

app = FastAPI(
    title="PDF Service",
    description="PDF extraction service for My Health Log",
    version="0.1.0",
)

app.include_router(extract.router)
app.include_router(health.router)
