from typing import Union

from fastapi import FastAPI
from .service_shortener.src.api import router as shortener_router
from .common.routers import router as common_router
from .service_shortener.src.alias_generator import AliasCounter
from .core.db import init_db
from .core import get_db, get_config, get_cache_counter_client
import redis

config = get_config()

app = FastAPI(
    title="URL Shortener Service",
    description="A simple URL shortener service built with FastAPI.",
    version="1.0.0",
)


@app.on_event("startup")
def setup_counter():

    app.state.alias_counter = AliasCounter(
        cache_client=get_cache_counter_client(),
        range_size=config.cache_counter_range_size,
    )


init_db()


app.include_router(shortener_router, prefix="/shortener", tags=["service_shortener"])
app.include_router(common_router)
