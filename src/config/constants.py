from enum import Enum

GEMINI_TEMPERATURE = 0.8  # 0-2
MAX_TOKENS_TAILOR = 10000
MAX_TOKENS_ATS = 2000


class ValidFileExtensions(Enum):
    TEXT = ".txt"
    LATEX = ".tex"
