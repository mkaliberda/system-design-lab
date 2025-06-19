import dotenv
import os
from pathlib import Path


class Config:

    def __init__(self):
        self.load_env()

    def load_env(self):
        env_path = Path(__file__).parent.parent / ".env"
        dotenv.load_dotenv(env_path)

    @property
    def db_url_shortener(self):
        return os.getenv(
            "DATABASE_URL_SHORTENER",
            "postgresql://postgres:password@localhost:5432/url_shortener_db",
        )

    @property
    def db_pool_size(self):
        return int(os.getenv("DB_SHORTENER_POOL_SIZE", "10"))

    @property
    def db_max_overflow(self):
        return int(os.getenv("DB_SHORTENER_MAX_OVERFLOW", "20"))


def get_config() -> Config:
    """
    Get the configuration for the URL shortener service.

    Returns:
        Config: Configuration instance for the URL shortener service.
    """
    return Config()
