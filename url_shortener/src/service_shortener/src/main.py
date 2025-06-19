from fastapi import FastAPI

from .service_shortener.api import router as service_router
from ...common.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="URL Shortener Service",
    description="A simple URL shortener service built with FastAPI.",
    version="1.0.0",
)

app.include_router(
    service_router,
)
