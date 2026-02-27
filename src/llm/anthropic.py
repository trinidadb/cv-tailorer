"""
LLM Client Manager - Handles Anthropic API interactions
"""

import anthropic

from src.config.constants import MAX_TOKENS_TAILOR, ANTHROPIC_TEMPERATURE, MAX_TOKENS_ATS
from src.config.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE, ATS_SYSTEM_PROMPT, ATS_USER_TEMPLATE, KEYWORDS_SYSTEM_PROMPT, KEYWORDS_USER_TEMPLATE
from src.config.schemas import TailoredResume, ATSScoreReport, ExtractedKeywords
from src.llm.base import BaseLLMClient, BaseLLMTailor, BaseLLMATS


class AnthropicClient(BaseLLMClient):

    def __init__(self, model: str = 'claude-sonnet-4-5', *args, **kwargs):
        self.model = model
        print(f"Provider: ANTHROPIC ------ Model:{model}")
        super().__init__(*args, **kwargs)

    def _init_client(self, *args, **kwargs):
        try:
            anthropic_client = anthropic.Anthropic()
            print("✓ Anthropic API initialized successfully")
            return anthropic_client
        except Exception as e:
            print(f"⚠ Anthropic initialization failed: {e}")

    def get_keywords(self, job_description: str, top_n: int = 30, system_prompt: str = None, user_prompt: str = None) -> ExtractedKeywords:
        system_prompt = system_prompt or KEYWORDS_SYSTEM_PROMPT
        user_prompt = user_prompt or KEYWORDS_USER_TEMPLATE

        response = self.client.messages.parse(
            model=self.model,
            max_tokens=10000,
            temperature=0,
            system=system_prompt.format(top_n=top_n),
            messages=[
                {"role": "user", "content": user_prompt.format(job_description=job_description)}
            ],
            output_format=ExtractedKeywords,
        )
        return response.parsed_output


class AnthropicTailor(AnthropicClient, BaseLLMTailor):

    def generate(self, system_prompt: str = None, user_prompt: str = None, temperature: float = ANTHROPIC_TEMPERATURE, max_tokens: int = MAX_TOKENS_TAILOR) -> str:

        print("[ANTHROPIC] GENERATE WITH UNSTRUCTURED OUTPUT ------- Temperature:{temperature}")

        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt or SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": user_prompt or USER_PROMPT_TEMPLATE}
            ]
        )
        return response.content[0].text

    def generate_with_structured_output(self, system_prompt: str = None, user_prompt: str = None, temperature: float = ANTHROPIC_TEMPERATURE, max_tokens: int = MAX_TOKENS_TAILOR) -> TailoredResume:

        print(f"[ANTHROPIC] GENERATE WITH STRUCTURED OUTPUT ------- Temperature:{temperature}")

        response = self.client.messages.parse(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt or SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": user_prompt or USER_PROMPT_TEMPLATE}
            ],
            output_format=TailoredResume,
        )
        return response.parsed_output

    def generate_then_extract_and_structure(self, system_prompt: str = None, user_prompt: str = None, temperature: float = ANTHROPIC_TEMPERATURE, max_tokens: int = MAX_TOKENS_TAILOR) -> TailoredResume:
        """Creative generation is unconstrained, extraction step is a simpler deterministic task."""

        print("[ANTHROPIC] GENERATE THEN EXTRACT AND STRUCTURE OUTPUT ------- Temperature:{temperature}")

        raw_text = self.generate(system_prompt=system_prompt, user_prompt=user_prompt, temperature=temperature, max_tokens=max_tokens)

        extraction_prompt = f"""
        Extract the resume sections from the text below into the required JSON format.
        Return ONLY the JSON, no commentary.

        RESUME TEXT:
        {raw_text}
        """

        response = self.client.messages.parse(
            model=self.model,
            max_tokens=max_tokens,
            temperature=0,
            messages=[
                {"role": "user", "content": extraction_prompt}
            ],
            output_format=TailoredResume,
        )
        return response.parsed_output


class AnthropicATS(AnthropicClient, BaseLLMATS):

    def score(self, resume_text: str, job_description: str) -> ATSScoreReport:
        user_prompt = ATS_USER_TEMPLATE.format(
            job_description=job_description,
            resume_text=resume_text,
        )

        response = self.client.messages.parse(
            model=self.model,
            max_tokens=MAX_TOKENS_ATS,
            temperature=0,
            system=ATS_SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": user_prompt}
            ],
            output_format=ATSScoreReport,
        )
        return response.parsed_output