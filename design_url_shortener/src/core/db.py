import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from .config import get_config

config = get_config()

engine = create_engine(
    config.db_url_shortener,
    pool_size=int(config.db_pool_size),
    max_overflow=int(config.db_max_overflow),
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# This is a base class that our table models will inherit from.
Base = declarative_base()


# This is our FastAPI dependency function. It yields a single database session
# for one request and ensures it's closed afterward.
def get_db():
    with SessionLocal() as session:
        try:
            yield session
        finally:
            session.close()


def init_db():
    """Initialize the database by creating all tables."""
    Base.metadata.create_all(bind=engine)
    print("Database initialized and tables created.")
