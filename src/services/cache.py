"""
Resume Cache
In-memory cache for TailoredResume objects.
Avoids re-running the LLM when the user switches between .tex and .docx formats.
"""

import uuid
from cachetools import TTLCache
from src.config.schemas import TailoredResume

# Stores up to 100 resumes, each expires after 1 hour
_cache: TTLCache = TTLCache(maxsize=100, ttl=3600)


def store(resume: TailoredResume) -> str:
    """Store a TailoredResume and return its unique ID."""
    resume_id = str(uuid.uuid4())
    _cache[resume_id] = resume
    return resume_id


def get(resume_id: str) -> TailoredResume | None:
    """Retrieve a TailoredResume by ID. Returns None if expired or not found."""
    return _cache.get(resume_id)