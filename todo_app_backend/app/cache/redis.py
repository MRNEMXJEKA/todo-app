import json

from redis import Redis


class RedisCacheBackend:
    def __init__(self, redis_url: str, cache_ttl_seconds: int | None = None):
        self.redis = Redis.from_url(redis_url, decode_responses=True)
        self.cache_ttl_seconds = cache_ttl_seconds

    def set(self, key: str, value: dict | list) -> None:
        self.redis.set(key, json.dumps(value), ex=self.cache_ttl_seconds)

    def get(self, key: str) -> dict | list | None:
        value = self.redis.get(key)
        if value is None:
            return None
        return json.loads(value)

    def delete(self, key: str) -> None:
        self.redis.delete(key)
