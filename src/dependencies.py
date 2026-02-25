from functools import lru_cache
from src.config.constants import ValidProviders, ValidModels
from src.llm.base import BaseLLMClient, BaseLLMATS, BaseLLMTailor
from src.llm.gemini import GeminiTailor, GeminiATS, GeminiClient
from src.llm.anthropic import AnthropicTailor, AnthropicATS, AnthropicClient
from src.services.tailor import CVTailor
from src.services.ats import ATSSystem

PROVIDERS = {
    ValidProviders.GEMINI:    (GeminiClient, GeminiTailor,    GeminiATS),
    ValidProviders.ANTHROPIC: (AnthropicClient, AnthropicTailor, AnthropicATS),
}

MODELS = {
    ValidProviders.GEMINI: [ValidModels.GEM_25_FLASH, ValidModels.GEM_25_FLASH_LITE, ValidModels.GEM_30, ValidModels.GEM_30_FLASH, ValidModels.GEM_31],
    ValidProviders.ANTHROPIC: [ValidModels.ANT_HAIKU, ValidModels.ANT_SONNET, ValidModels.ANT_OPUS],
}


@lru_cache  # So it's only defined once
def get_client_provider(model: ValidModels = ValidModels.GEM_25_FLASH) -> BaseLLMClient:
    provider = ValidProviders.GEMINI if model in MODELS[ValidProviders.GEMINI] else ValidProviders.ANTHROPIC
    client, _, _ = PROVIDERS[provider]
    return client(model=model.value)


@lru_cache  # So it's only defined once
def get_tailor_provider(model: ValidModels = ValidModels.GEM_25_FLASH) -> BaseLLMTailor:
    provider = ValidProviders.GEMINI if model in MODELS[ValidProviders.GEMINI] else ValidProviders.ANTHROPIC
    _, tailorer, _ = PROVIDERS[provider]
    return tailorer(model=model.value)


@lru_cache  # So it's only defined once
def get_ats_provider(model: ValidModels = ValidModels.GEM_25_FLASH) -> BaseLLMATS:
    provider = ValidProviders.GEMINI if model in MODELS[ValidProviders.GEMINI] else ValidProviders.ANTHROPIC
    _, _, ats = PROVIDERS[provider]
    return ats(model=model.value)


def get_tailor(model: ValidModels = ValidModels.GEM_25_FLASH) -> CVTailor:
    return CVTailor(tailorer=get_tailor_provider(model=model))


def get_ats(model: ValidModels = ValidModels.GEM_25_FLASH) -> ATSSystem:
    return ATSSystem(ats=get_ats_provider(model=model))
