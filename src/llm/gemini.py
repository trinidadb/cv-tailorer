"""
LLM Client Manager - Handles Anthropic and Gemini API interactions
"""

import os
from dotenv import load_dotenv

from config.constants import MAX_TOKENS, GEMINI_TEMPERATURE
from config.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from src.llm.base import BaseLLMClient


class GeminiClient(BaseLLMClient):

    def __init__(self, model: str = 'gemini-2.5-flash', *args, **kwargs):
        self.model = model
        super().__init__(*args, **kwargs)

    def _init_llm(self, *args, **kwargs):
        try:
            import google.generativeai as genai
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            gemini_client = genai.GenerativeModel(self.model)
            print("✓ Gemini API initialized successfully")
            return gemini_client
        except Exception as e:
            print(f"⚠ Gemini initialization failed: {e}")

    def generate(self, system_prompt: str = None, user_prompt: str = None, max_tokens: int = MAX_TOKENS) -> str:
        system_prompt = system_prompt or SYSTEM_PROMPT
        user_prompt = user_prompt or USER_PROMPT_TEMPLATE
        full_prompt = f"{system_prompt}\n\n{user_prompt}"

        response = self.llm.generate_content(
            full_prompt,
            generation_config={
                "max_output_tokens": max_tokens,
                "temperature": GEMINI_TEMPERATURE,
            }
        )

        return response.text
