from functools import lru_cache
from src.llm.gemini import GeminiTailor, GeminiATS, GeminiClient
from src.services.tailor import CVTailor
from src.services.ats import ATSSystem


@lru_cache  # So it's only defined once
def get_gemini_client() -> GeminiClient:
    return GeminiClient()


@lru_cache  # So it's only defined once
def get_gemini_tailor() -> GeminiTailor:
    return GeminiTailor()


@lru_cache  # So it's only defined once
def get_gemini_ats() -> GeminiATS:
    return GeminiATS()


def get_tailor() -> CVTailor:
    return CVTailor(tailorer=get_gemini_tailor())


def get_ats() -> ATSSystem:
    return ATSSystem(ats=get_gemini_ats())