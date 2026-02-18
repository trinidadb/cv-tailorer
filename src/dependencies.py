from functools import lru_cache
from src.llm.gemini import GeminiClient
from src.services.tailor import CVTailor


@lru_cache  # So it's only defined once
def get_gemini_llm_client() -> GeminiClient:
    return GeminiClient()

@lru_cache
def get_tailor() -> CVTailor:
    return CVTailor(llm_client=get_gemini_llm_client())
