from enum import Enum

GEMINI_TEMPERATURE = 0.8  # 0-2
ANTHROPIC_TEMPERATURE = 0.3 # 0-1
MAX_TOKENS_TAILOR = 14000
MAX_TOKENS_ATS = 14000


class ValidFileExtensions(Enum):
    TEXT = ".txt"
    LATEX = ".tex"
    DOCX = ".docx" 


class ValidKeyExtractorMethods(Enum):
    RANK_TF_IDF = "rank_tf_idf"
    GRAPH_BASED = "graph_based"
    LINGUISITC_SEMANTIC = "ling_semantic"
    KEYBERT = "keybert"


class ValidProviders(Enum):
    GEMINI = "gemini"
    ANTHROPIC = "anthropic"


class ValidModels(Enum):
    ANT_SONNET = "claude-sonnet-4-5"
    ANT_HAIKU = "claude-haiku-4-5"
    ANT_OPUS = "claude-opus-4-6"
    GEM_25_FLASH = "gemini-2.5-flash"
    GEM_25_FLASH_LITE = "gemini-2.5-flash-lite"
    GEM_30 = "gemini-3-pro-preview"
    GEM_30_FLASH = "gemini-3-flash-preview"
    GEM_31 = "gemini-3.1-pro-preview"


class ValidLanguages(Enum):
    EN = "english"
    ES = "spanish"
