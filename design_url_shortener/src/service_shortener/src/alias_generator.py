import abc
import string
import random
from .config import get_config
from .alias_counter import AliasCounter
from ...models import URL

config = get_config()


class AbstractAliasStrategy(abc.ABC):

    @abc.abstractmethod
    def generate_alias(self, length) -> str:
        pass


class CounterAliasStrategy(AbstractAliasStrategy):

    ALPHABET = string.ascii_letters + string.digits  # Base62 characters

    def __init__(self, alias_counter: AliasCounter):
        if not isinstance(alias_counter, AliasCounter):
            raise TypeError("alias_counter must be an instance of AliasCounter.")
        self.alias_counter = alias_counter

    def _encode_to_base62(self, num: int) -> str:
        """Converts an integer to a base62 string."""
        if num == 0:
            return self.ALPHABET[0]
        base62 = []
        base = len(self.ALPHABET)
        while num > 0:
            remainder = num % base
            base62.append(self.ALPHABET[remainder])
            num //= base
        return "".join(reversed(base62))

    def generate_alias(self, length) -> str:
        """
        Generates a unique alias from an incrementing counter (from memcache)
        using the provided session and memcache client for alias existence checks.
        """
        # Counter logic now uses memcache_client
        counter_value = self.alias_counter.next()
        alias = self._encode_to_base62(counter_value)
        print(f"Generated alias: {alias} from counter value: {counter_value}")

        if len(alias) < length:
            # fill leading chars
            alias = self.ALPHABET[0] * (length - len(alias)) + alias

        return alias


class RandomAliasStrategy(AbstractAliasStrategy):
    """
    Generates aliases using random characters and ensures uniqueness by
    checking against the database.
    """

    ALPHABET = string.ascii_letters + string.digits  # Alphanumeric characters

    def _generate_random_string(self, length: int) -> str:
        """Generates a random string of specified length."""
        return "".join(random.choice(self.ALPHABET) for _ in range(length))

    def generate_alias(self, length) -> str:
        """
        Generates a unique random alias using the provided session and memcache client.
        Retries if a collision is found.
        """
        alias = self._generate_random_string(length)
        return alias


class AliasGenerator:

    def __init__(self, strategy: AbstractAliasStrategy):
        if not isinstance(strategy, AbstractAliasStrategy):
            raise TypeError("Strategy must be an instance of AbstractAliasStrategy.")
        self._strategy = strategy

    def set_strategy(self, strategy: AbstractAliasStrategy):
        """
        Allows changing the alias generation strategy at runtime.
        """
        if not isinstance(strategy, AbstractAliasStrategy):
            raise TypeError("Strategy must be an instance of AbstractAliasStrategy.")
        self._strategy = strategy

    def check_alias_exists(self, db, alias: str) -> bool:
        """
        Checks if the alias already exists in the database.
        """
        existing_url = db.query(URL).filter(URL.alias == alias).first()
        return existing_url is not None

    def generate_alias(self, db, length=None, retries=None) -> str:
        """
        Delegates the alias generation to the current strategy.
        """
        if length is None:
            length = config.alias_generation_length

        if retries is None:
            retries = config.alias_generation_retries

        for _ in range(retries):
            alias = self._strategy.generate_alias(length)
            if not self.check_alias_exists(db, alias):
                return alias
        raise RuntimeError("Failed to generate a unique alias after retries.")


def get_alias_generator(alias_counter: AliasCounter) -> AliasGenerator:
    """
    Returns a default alias generator with the CounterAliasStrategy.
    This can be used as a singleton instance in the application.
    """
    strategy_type = config.alias_generation_strategy
    if strategy_type == config.COUNTER_ALIAS_GENERATION:
        strategy = CounterAliasStrategy(alias_counter)
    else:
        strategy = RandomAliasStrategy()

    return AliasGenerator(strategy)
