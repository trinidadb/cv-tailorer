"""
LLM Client Manager - Handles Anthropic and Gemini API interactions
"""

import os
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from typing import Optional, Literal

from config.constants import MAX_TOKENS, GEMINI_TEMPERATURE
from config.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

load_dotenv()


class BaseLLMClient(ABC):

    def __init__(self, *args, **kwargs):
        self.llm = self._init_llm(args, kwargs)

    @abstractmethod
    def _init_llm(self, *args, **kwargs):
        pass

    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str, max_tokens: int = MAX_TOKENS) -> str:
        pass
