import redis
from .config import get_config
import redis

config = get_config()


class CacheCounterCient:
    """
    A client for managing cache counters using Redis.
    """

    def __init__(self, redis_client=config.cache_counter_host):
        if redis_client is None:
            redis_client = redis.Redis.from_url(config.cache_counter_host)
        self.redis_client = redis_client

    def refresh_connection(self):
        """
        Refreshes the Redis connection to ensure it is active.
        """
        try:
            self.redis_client.ping()
        except redis.exceptions.ConnectionError:
            try:
                self.redis_client.close()
            except Exception:
                pass  # Ignore errors if the client does not support close()
            self.redis_client = redis.Redis.from_url(get_config().cache_counter_host)

    def get(self, key: str) -> int:
        """
        Retrieves the value of a counter from Redis.
        """
        value = self.redis_client.get(key)
        return int(value) if value else 0

    def increment(self, key: str, amount: int = 1) -> int:
        """
        Increments the counter by a specified amount.
        """
        return self.redis_client.incrby(key, amount)


def get_cache_counter_client() -> CacheCounterCient:
    """
    Return alwasys Redis based cache counter client.

    Returns:
        CacheCounterCient: Cache counter client instance.
    """
    return CacheCounterCient(
        redis_client=redis.Redis.from_url(config.cache_counter_host)
    )
