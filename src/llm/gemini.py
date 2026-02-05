"""
LLM Client Manager - Handles Anthropic and Gemini API interactions
"""

from google import genai
from google.genai import types as genaiTypes

from config.constants import MAX_TOKENS, GEMINI_TEMPERATURE
from config.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from src.llm.base import BaseLLMClient


class GeminiClient(BaseLLMClient):

    def __init__(self, model: str = 'gemini-2.5-flash', *args, **kwargs):
        self.model = model
        super().__init__(*args, **kwargs)

    def _init_client(self, *args, **kwargs):
        try:
            gemini_client = genai.Client()
            print("✓ Gemini API initialized successfully")
            return gemini_client
        except Exception as e:
            print(f"⚠ Gemini initialization failed: {e}")

    def generate(self, system_prompt: str = None, user_prompt: str = None, temperature: int = GEMINI_TEMPERATURE, max_tokens: int = MAX_TOKENS) -> str:
        system_prompt = system_prompt or SYSTEM_PROMPT
        user_prompt = user_prompt or USER_PROMPT_TEMPLATE
        full_prompt = f"{system_prompt}\n\n{user_prompt}"

        response = self.client.models.generate_content(
            model=self.model,
            contents=full_prompt,
            config=genaiTypes.GenerateContentConfig(
                temperature=temperature,  # Ajusta entre 0.0 y 2.0 (mayor = más creativo)
                max_output_tokens=max_tokens
            )
        )

        return response.text
