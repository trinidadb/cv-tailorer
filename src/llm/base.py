"""
LLM Client Manager - Handles Anthropic and Gemini API interactions
"""

from abc import ABC, abstractmethod

from src.config.constants import MAX_TOKENS


class BaseLLMClient(ABC):

    def __init__(self, *args, **kwargs):
        self.client = self._init_client(args, kwargs)

    @abstractmethod
    def _init_client(self, *args, **kwargs):
        pass

    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str, temperature: int = None, max_tokens: int = MAX_TOKENS) -> str:
        pass
