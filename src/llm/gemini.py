"""
LLM Client Manager - Handles Anthropic and Gemini API interactions
"""

from google import genai
from google.genai import types as genaiTypes

from config.constants import MAX_TOKENS, GEMINI_TEMPERATURE
from config.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from config.schemas import TailoredResume
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

    def _generate_full_prompt(self, system_prompt: str = None, user_prompt: str = None):
        system_prompt = system_prompt or SYSTEM_PROMPT
        user_prompt = user_prompt or USER_PROMPT_TEMPLATE
        return f"{system_prompt}\n\n{user_prompt}"

    def generate(self, system_prompt: str = None, user_prompt: str = None, temperature: int = GEMINI_TEMPERATURE, max_tokens: int = MAX_TOKENS) -> str:

        print("GENERATE WITH UNSTRUCTURED OUTPUT")

        full_prompt = self._generate_full_prompt(system_prompt=system_prompt, user_prompt=user_prompt)

        response = self.client.models.generate_content(
            model=self.model,
            contents=full_prompt,
            config=genaiTypes.GenerateContentConfig(
                temperature=temperature,  # Ajusta entre 0.0 y 2.0 (mayor = más creativo)
                max_output_tokens=max_tokens,
            )
        )

        return response.text

    def generate_with_structured_output(self, system_prompt: str = None, user_prompt: str = None, temperature: int = GEMINI_TEMPERATURE, max_tokens: int = MAX_TOKENS) -> TailoredResume:

        print("GENERATE WITH STRUCTURED OUTPUT")

        full_prompt = self._generate_full_prompt(system_prompt=system_prompt, user_prompt=user_prompt)

        response = self.client.models.generate_content(
            model=self.model,
            contents=full_prompt,
            config=genaiTypes.GenerateContentConfig(
                temperature=temperature,  # Ajusta entre 0.0 y 2.0 (mayor = más creativo)
                max_output_tokens=max_tokens,
                response_mime_type="application/json",
                response_schema=TailoredResume
            )
        )

        return response.parsed


    def generate_then_extract_and_structure(self, system_prompt: str = None, user_prompt: str = None, temperature: int = GEMINI_TEMPERATURE, max_tokens: int = MAX_TOKENS):
        '''This way the creative generation is unconstrained, and the extraction step is a much simpler task that rarely degrades quality.'''

        print("GENERATE THEN EXTRACT AND STRUCTURE OUTPUT")

        raw_text = self.generate(system_prompt=system_prompt, user_prompt=user_prompt, temperature=temperature, max_tokens=max_tokens)

        extraction_prompt = f"""
        Extract the resume sections from the text below into the required JSON format.
        Return ONLY the JSON, no commentary.

        RESUME TEXT:
        {raw_text}
        """
        response = self.client.models.generate_content(
            model=self.model,
            contents=extraction_prompt,
            config=genaiTypes.GenerateContentConfig(
                temperature=0,  # deterministic for extraction
                response_mime_type="application/json",
                response_schema=TailoredResume
            )
        )
        return response.parsed
