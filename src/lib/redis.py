import redis
from typing import Optional, Any
import json

from src.configs.constants import RedisKeyCategory
from src.configs.env import get_settings

config = get_settings()

class Redis:
    def __init__(self, prefix: str = "url_shortener"):
        self.client = redis.Redis.from_url(f'redis://{config.redis_host}:{config.redis_port}', decode_responses=True)
        self.prefix = prefix

    def _key(self, category: str, identifier: str) -> str:
        """Generate a namespaced Redis key"""
        return f"{self.prefix}:{category}:{identifier}"

    # --------------------
    # Rate Limiting
    # --------------------
    def is_allowed(self, identity: str, scope: str, limit: int, window: int) -> bool:
        """
        :param identity: is unique identifier - ip or user_id perhaps
        :param scope: is action like - shorten or redirect or get_otp
        :param limit: is how many times a user can perform an activity
        :param window: is basically ttl (time to live)
        :return: boolean: whether user can perform an activity ot not
        """
        key = self._key(RedisKeyCategory.RATE_LIMIT, f"{scope}:{identity}")
        count = self.client.incr(key)

        if count == 1:
            self.client.expire(key, window)

        return count <= limit

    def get_ttl(self, identity: str, scope: str) -> Optional[int]:
        key = self._key(RedisKeyCategory.RATE_LIMIT, f"{scope}:{identity}")
        return self.client.ttl(key)

    def reset_rate_limit(self, identity: str, scope: str) -> None:
        key = self._key(RedisKeyCategory.RATE_LIMIT, f"{scope}:{identity}")
        self.client.delete(key)

    # --------------------
    # Generic Cache Methods
    # --------------------
    def set_cache(self, category: str, identifier: str, value: Any, ttl: int = 300) -> None:
        """
        Cache any JSON-serializable value.
        Args:
            category: logical bucket name (e.g. 'url', 'user', 'session')
            identifier: key inside category
            value: any JSON-serializable data
            ttl: time-to-live in seconds
        """
        key = self._key(category, identifier)
        self.client.set(key, json.dumps(value), ex=ttl)

    def get_cache(self, category: str, identifier: str) -> Optional[Any]:
        """
        Fetch cached value. Returns deserialized data.
        """
        key = self._key(category, identifier)
        value = self.client.get(key)
        return json.loads(value) if value else None

    def delete_cache(self, category: str, identifier: str) -> None:
        """
        Delete cached value.
        """
        key = self._key(category, identifier)
        self.client.delete(key)


redis_cache = Redis()