import string

from .config import get_config

config = get_config()


class AliasCounter:
    def __init__(
        self, cache_client, range_size=100, cache_key=config.cache_counter_key
    ):
        self.cache_client = cache_client
        self.range_size = range_size
        self.cache_key = cache_key
        self.start, self.end = self._reserve_range()
        self.current = self.start

    def _refresh_connection(self):
        """
        Refreshes the Cache connection to ensure it is active.
        """
        self.cache_client.refresh_connection()

    def _reserve_range(self):
        self._refresh_connection()
        end = self.cache_client.increment(self.cache_key, self.range_size)
        start = end - self.range_size + 1
        return start, end

    def next(self):
        if self.current > self.end:
            self.start, self.end = self._reserve_range()
            self.current = self.start

        val = self.current
        self.current += 1  # increment safely within the lock

        return val
