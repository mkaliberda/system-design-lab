from ...core.config import Config
import os


class ShortenerConfig(Config):
    """
    Configuration class for URL shortener service.
    Inherits from the core Config class.
    """

    RANDOM_ALIAS_GENERATION = "random"
    COUNTER_ALIAS_GENERATION = "counter"

    def __init__(self):
        super().__init__()

    @property
    def alias_generation_length(self):
        return int(os.getenv("ALIAS_GENERATION_LENGTH", 7))

    @property
    def alias_generation_retries(self):
        return int(os.getenv("ALIAS_GENERATION_RETRIES", 5))

    @property
    def alias_generation_strategy(self):
        return os.getenv(
            "ALIAS_GENERATION_STRATEGY", self.RANDOM_ALIAS_GENERATION
        ).lower()


def get_config() -> ShortenerConfig:
    """
    Get the configuration for the URL shortener service.

    Returns:
        ShortenerConfig: Configuration instance for the URL shortener service.
    """
    return ShortenerConfig()
