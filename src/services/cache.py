"""
Resume Cache
In-memory cache for TailoredResume objects.
Avoids re-running the LLM when the user switches between .tex and .docx formats.

If you want replace the in-memory TTLCache with Redis so cache survives container
restarts and works across multiple workers.

"""
import os
import uuid
from cachetools import TTLCache
import redis
from src.config.schemas import TailoredResume

TTL_SECONDS = 3600


class TTLCacheBackend:
    def __init__(self):
        self._cache = TTLCache(maxsize=100, ttl=TTL_SECONDS)

    def store(self, resume: TailoredResume) -> str:
        resume_id = str(uuid.uuid4())
        self._cache[resume_id] = resume
        return resume_id

    def get(self, resume_id: str) -> TailoredResume | None:
        return self._cache.get(resume_id)


class RedisCacheBackend:
    def __init__(self):
        self._pool = redis.ConnectionPool(
            host=os.getenv("REDIS_HOST"),
            port=int(os.getenv("REDIS_PORT")),
            decode_responses=True,
        )

    def store(self, resume: TailoredResume) -> str:
        resume_id = str(uuid.uuid4())
        redis.Redis(connection_pool=self._pool).setex(
            name=resume_id,
            time=TTL_SECONDS,
            value=resume.model_dump_json(),
        )
        return resume_id

    def get(self, resume_id: str) -> TailoredResume | None:
        data = redis.Redis(connection_pool=self._pool).get(resume_id)
        return TailoredResume.model_validate_json(data) if data else None


def _make_cache():
    if os.getenv("REDIS_MODE") == "true":
        return RedisCacheBackend()
    return TTLCacheBackend()


# Single instance used across the app
_backend = _make_cache()

def store(resume: TailoredResume) -> str:
    return _backend.store(resume)

def get(resume_id: str) -> TailoredResume | None:
    return _backend.get(resume_id)