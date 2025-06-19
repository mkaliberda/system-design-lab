from typing import Union

from fastapi import FastAPI
from .service_shortener.src.api import router as shortener_router
from .common.routers import router as common_router
from .core.db import init_db

app = FastAPI(
    title="URL Shortener Service",
    description="A simple URL shortener service built with FastAPI.",
    version="1.0.0",
)


init_db()


app.include_router(shortener_router, prefix="/shortener", tags=["service_shortener"])
app.include_router(common_router)
