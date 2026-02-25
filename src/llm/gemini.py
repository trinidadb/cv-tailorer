"""
LLM Client Manager - Handles Gemini API interactions
"""

from google import genai
from google.genai import types as genaiTypes

from src.config.constants import MAX_TOKENS_TAILOR, GEMINI_TEMPERATURE, MAX_TOKENS_ATS
from src.config.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE, ATS_SYSTEM_PROMPT, ATS_USER_TEMPLATE, KEYWORDS_SYSTEM_PROMPT, KEYWORDS_USER_TEMPLATE
from src.config.schemas import TailoredResume, ATSScoreReport, ExtractedKeywords
from src.llm.base import BaseLLMClient, BaseLLMTailor, BaseLLMATS


class GeminiClient(BaseLLMClient):

    def __init__(self, model: str = 'gemini-2.5-flash', *args, **kwargs):
        self.model = model
        print(f"Provider: GEMINI ------ Model:{model}")
        super().__init__(*args, **kwargs)

    def _init_client(self, *args, **kwargs):
        try:
            gemini_client = genai.Client()
            print("✓ Gemini API initialized successfully")
            return gemini_client
        except Exception as e:
            print(f"⚠ Gemini initialization failed: {e}")

    def get_keywords(self, job_description: str, top_n: int = 30, system_prompt: str = None, user_prompt: str = None) -> ExtractedKeywords:
        system_prompt = system_prompt or KEYWORDS_SYSTEM_PROMPT
        user_prompt = user_prompt or KEYWORDS_USER_TEMPLATE

        response = self.client.models.generate_content(
            model=self.model,
            contents=f"{system_prompt.format(top_n=top_n)}\n\n{user_prompt.format(job_description=job_description)}",
            config=genaiTypes.GenerateContentConfig(
                temperature=0,          # deterministic — same JD should always give same keywords
                max_output_tokens=10000,
                response_mime_type="application/json",
                response_schema=ExtractedKeywords,
            ),
        )
        return response.parsed


class GeminiTailor(GeminiClient, BaseLLMTailor):

    def _generate_full_prompt(self, system_prompt: str = None, user_prompt: str = None):
        system_prompt = system_prompt or SYSTEM_PROMPT
        user_prompt = user_prompt or USER_PROMPT_TEMPLATE
        return f"{system_prompt}\n\n{user_prompt}"

    def generate(self, system_prompt: str = None, user_prompt: str = None, temperature: int = GEMINI_TEMPERATURE, max_tokens: int = MAX_TOKENS_TAILOR ) -> str:

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

    def generate_with_structured_output(self, system_prompt: str = None, user_prompt: str = None, temperature: int = GEMINI_TEMPERATURE, max_tokens: int = MAX_TOKENS_TAILOR ) -> TailoredResume:

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

    def generate_then_extract_and_structure(self, system_prompt: str = None, user_prompt: str = None, temperature: int = GEMINI_TEMPERATURE, max_tokens: int = MAX_TOKENS_TAILOR ):
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


class GeminiATS(GeminiClient, BaseLLMATS):

    def score(self, resume_text: str, job_description: str) -> ATSScoreReport:
        user_prompt = ATS_USER_TEMPLATE.format(
            job_description=job_description,
            resume_text=resume_text,
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=f"{ATS_SYSTEM_PROMPT}\n\n{user_prompt}",
            config=genaiTypes.GenerateContentConfig(
                temperature=0,          # deterministic — scoring should be consistent
                max_output_tokens=MAX_TOKENS_ATS,
                response_mime_type="application/json",
                response_schema=ATSScoreReport,
            ),
        )
        return response.parsed