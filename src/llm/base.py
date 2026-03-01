from abc import ABC, abstractmethod
from src.config.constants import MAX_TOKENS_TAILOR, ValidLanguages
from src.config.schemas import ExtractedKeywords


class BaseLLMClient(ABC):
    """Handles client initialization only"""
    def __init__(self, *args, **kwargs):
        self.client = self._init_client()

    @abstractmethod
    def _init_client(self):
        pass

    @abstractmethod
    def get_keywords(self, job_description: str, top_n: int = 30, *args, **kwargs) -> ExtractedKeywords:
        pass


class BaseLLMTailor(ABC):
    """Interface for tailor-specific LLM methods"""

    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str, temperature: float = None, max_tokens: int = MAX_TOKENS_TAILOR) -> str:
        pass

    @abstractmethod
    def generate_with_structured_output(self, system_prompt: str, user_prompt: str, temperature: float = None, max_tokens: int = MAX_TOKENS_TAILOR):
        pass

    @abstractmethod
    def generate_then_extract_and_structure(self, system_prompt: str, user_prompt: str, temperature: float = None, max_tokens: int = MAX_TOKENS_TAILOR):
        pass


class BaseLLMATS(ABC):
    """Interface for ATS scorer-specific LLM methods"""

    @abstractmethod
    def score(self, resume_text: str, job_description: str):
        pass
